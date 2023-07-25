from fastapi import APIRouter
from models import Menus, Submenus, Dishes
import sys
from fastapi.responses import JSONResponse
from fastapi import HTTPException

sys.path.append("..")

router = APIRouter()


async def get_dishe_content(id, title, description, price):
    content = (
        {
            "id":  str(id),
            "title":  title,
            "description":  description,
            "price": str(price),
        }
    )
    return content


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",)
async def get_dishes(menu_id: str, submenu_id: str):
    content = []
    all_dishes = await Dishes.filter(submenu__menu__id=menu_id, submenu__id=submenu_id)
    if not all_dishes:
        return JSONResponse(content=content)
    for dishe in all_dishes:
        content.append(await get_dishe_content(dishe.id, dishe.title, dishe.description, dishe.price))
    return JSONResponse(content=content)


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
async def get_dishe(menu_id: str, submenu_id: str, dishes_id: str):
    result = await Dishes.filter(submenu__id=submenu_id, submenu__menu__id=menu_id, id=dishes_id).first()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="dish not found"
        )
    else:
        content = await get_dishe_content(result.id, result.title, result.description, result.price)
        return JSONResponse(content=content)


# type: ignore
@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",)
async def create_dishe(menu_id: str, submenu_id: str, dishe: dict):
    find_menu = await Menus.filter(id=menu_id).first()
    if not find_menu:
        content = {'detail': 'menu does not exist'}
        return JSONResponse(status_code=200, content=content)
    find_submenu = await Submenus.filter(id=submenu_id).first()
    if not find_submenu:
        content = {'detail': 'submenu does not exist'}
        return JSONResponse(status_code=200, content=content)
    dishe_obj = await Dishes.create(
        title=dishe.get('title'),
        description=dishe.get('description'),
        price=dishe.get('price'),
        submenu_id=find_submenu.id,
    )
    await dishe_obj.save()
    content = await get_dishe_content(dishe_obj.id, dishe_obj.title,
                                      dishe_obj.description, dishe_obj.price)
    return JSONResponse(status_code=201, content=content)


@router.put("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
async def update_dishe(menu_id: str, submenu_id: str, dishes_id: str, dishe: dict):
    find_menu = await Menus.filter(id=menu_id).first()
    if not find_menu:
        content = {'detail': 'menu does not exist'}
        return JSONResponse(status_code=200, content=content)
    find_submenu = await Submenus.filter(id=submenu_id, menu__id=menu_id).first()
    if not find_submenu:
        content = {'detail': 'submenus does not exist'}
        return JSONResponse(status_code=200, content=content)
    find_dish = await Dishes.filter(id=dishes_id, submenu=find_submenu, submenu__menu=find_menu).first()
    if not find_dish:
        content = {'detail': 'dish does not exist'}
        return JSONResponse(status_code=200, content=content)
    find_dish.title = dishe.get('title')
    find_dish.description = dishe.get('description')
    find_dish.price = dishe.get('price')
    await find_dish.save()
    find_dish = await Dishes.filter(id=dishes_id, submenu__id=submenu_id, submenu__menu__id=menu_id).first()
    content = await get_dishe_content(find_dish.id, find_dish.title, find_dish.description, find_dish.price)
    return JSONResponse(status_code=200, content=content)


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dishes_id}")
async def delete_dishe(menu_id: str, submenu_id: str, dishes_id: str):
    deleted_count = await Dishes.filter(submenu__id=submenu_id, submenu__menu__id=menu_id, id=dishes_id).first()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Dishes {dishes_id} not found")
    await deleted_count.delete()
    content = {
        "status": True,
        "message": "The dishe has been deleted"
    }
    return JSONResponse(content=content)
