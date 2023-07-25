from fastapi import APIRouter
from models import Menus, Submenus, Dishes
import sys
from fastapi.responses import JSONResponse
from fastapi import HTTPException

sys.path.append("..")

router = APIRouter()


async def get_submenu_content(id, title, description):
    dishes_count = await Dishes.filter(submenu__id=id).count()
    content = (
        {
            "id":  str(id),
            "title":  title,
            "description":  description,
            "dishes_count": dishes_count,
        }
    )
    return content


@router.get("/api/v1/menus/{menu_id}/submenus",)
async def get_submenus(menu_id: str):
    content = []
    all_submenus = await Submenus.filter(menu__id=menu_id)
    if not all_submenus:
        return JSONResponse(content=content)
    for submenu in all_submenus:
        content.append(await get_submenu_content(submenu.id, submenu.title, submenu.description))
    return JSONResponse(content=content)


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id: str, submenu_id: str):
    # result = await Submenus.filter(Q(menu__id=menu_id, id=submenu_id))
    result = await Submenus.filter(menu__id=menu_id, id=submenu_id).first()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="submenu not found"
        )
    else:
        content = await get_submenu_content(result.id, result.title, result.description)
        return JSONResponse(content=content)


@router.post("/api/v1/menus/{menu_id}/submenus", )  # type: ignore
async def create_submenu(menu_id: str, submenu: dict):
    find_menu = await Menus.filter(id=menu_id).first()
    if not find_menu:
        content = {'detail': 'menu does not exist'}
        return JSONResponse(status_code=200, content=content)
    submenu_obj = await Submenus.create(
        title=submenu.get('title'),
        description=submenu.get('description'),
        menu_id=find_menu.id,
    )
    await submenu_obj.save()
    content = await get_submenu_content(submenu_obj.id, submenu_obj.title, submenu_obj.description)
    return JSONResponse(status_code=201, content=content)


@router.put("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def update_submenu(menu_id: str, submenu_id: str, submenu: dict):
    find_menu = await Menus.filter(id=menu_id)
    if not find_menu:
        content = {'detail': 'menu does not exist'}
        return JSONResponse(status_code=200, content=content)
    find_submenu = await Submenus.filter(id=submenu_id, menu__id=menu_id).first()
    if not find_submenu:
        content = {'detail': 'submenus does not exist'}
        return JSONResponse(status_code=200, content=content)
    find_submenu.title = submenu.get('title')
    find_submenu.description = submenu.get('description')
    await find_submenu.save()
    find_submenu = await Submenus.filter(id=submenu_id, menu__id=menu_id).first()
    content = await get_submenu_content(find_submenu.id, find_submenu.title, find_submenu.description)
    return JSONResponse(status_code=200, content=content)


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: str, submenu_id: str):
    deleted_count = await Submenus.filter(id=submenu_id, menu__id=menu_id).first()
    if not deleted_count:
        raise HTTPException(
            status_code=200, detail=f"Submenu {submenu_id} not found")
    await deleted_count.delete()
    content = {
        "status": True,
        "message": "The submenu has been deleted"
    }
    return JSONResponse(content=content)
