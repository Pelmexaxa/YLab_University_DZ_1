from fastapi import APIRouter
from models import Menus, Submenus, Dishes, \
    MenuIn_Pydantic
import sys
from fastapi.responses import JSONResponse
from fastapi import HTTPException

sys.path.append("..")

router = APIRouter()


async def get_menu_content(id, title, description):
    submenus_count = await Submenus.filter(menu__id=id).count()
    dishes_count = await Dishes.filter(submenu__menu__id=id).count()
    content = (
        {
            "id":  str(id),
            "title":  title,
            "description":  description,
            "submenus_count": submenus_count,
            "dishes_count": dishes_count,
        }
    )
    return content


@router.get("/api/v1/menus",)
async def get_menus():
    content = []
    all_menus = await Menus.all()
    if not all_menus:
        return JSONResponse(content=content)
    for menu in all_menus:
        content.append(await get_menu_content(menu.id, menu.title, menu.description))
    return JSONResponse(content=content)


@router.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: str):
    result = await Menus.filter(id=menu_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="menu not found"
        )
    else:
        content = await get_menu_content(result[0].id, result[0].title, result[0].description)
        return JSONResponse(content=content)


@router.post("/api/v1/menus", )  # type: ignore
async def create_menu(menu: MenuIn_Pydantic):
    menu_obj = await Menus.create(**menu.dict(exclude_unset=True))
    content = await get_menu_content(menu_obj.id, menu_obj.title, menu_obj.description)
    return JSONResponse(status_code=201, content=content)


@router.put("/api/v1/menus/{menu_id}",)
async def update_menu(menu_id: str, menu: MenuIn_Pydantic):
    result = await Menus.filter(id=menu_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="menu not found"
        )
    else:
        await Menus.filter(id=menu_id).update(**menu.dict(exclude_unset=True))
        result = await Menus.filter(id=menu_id)
        content = await get_menu_content(result[0].id, result[0].title, result[0].description)
        return JSONResponse(content=content)


@router.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: str):
    deleted_count = await Menus.filter(id=menu_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Menu {menu_id} not found")
    content = {
        "status": True,
        "message": "The menu has been deleted"
    }
    return JSONResponse(content=content)
