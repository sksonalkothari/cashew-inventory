import httpx
from app.utils.timestamp_utils import current_timestamp
from app.config import SUPABASE_URL
from app.exceptions.exceptions import GradeError
from app.utils.logger import logger
from app.utils.supabase_query import supabase_query

TABLE = "grades"

async def insert_or_reactivate_grade(data: dict, headers: dict):
    logger.info(f"Creating grade: {data['grade_name']}")
    try:
        existing = await supabase_query("grades", {"grade_name": f"eq.{data['grade_name']}"}, "id", headers)

        if existing:
           logger.info(f"Grade {data['grade_name']} already exists. Reactivating it.")
           modified_data = {
               "id":existing[0]["id"], 
               "is_deleted" : False,
               "updated_by": data["created_by"]
               }
           await soft_delete_grade(modified_data, headers)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SUPABASE_URL}/rest/v1/{TABLE}",
                    headers=headers,
                    json=[data]
                )
                logger.debug(response.status_code)
                logger.debug(response)
                
                if response.status_code >= 400:
                    result = response.json()
                    error_msg = result.get("msg") or result.get("error", {}).get("message") or response.text
                    raise GradeError(f"Grade creation failed: {error_msg}", status_code=response.status_code)
        return f"Grade {data['grade_name']} created/reactivated successfully"
    except GradeError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during insert or reactivate grade {data['grade_name']}")
        raise GradeError("Unexpected error", status_code=500)

async def update_grade(data: dict, headers: dict):
    logger.info(f"Updating grade ID {data['id']}")
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{data['id']}",
            headers=headers,
            json={
                "grade_name": data["grade_name"],
                "updated_by": data["updated_by"],
                "updated_at": current_timestamp()
            }
        )
        result = response.json()
        if response.status_code >= 400:
            raise GradeError(f"Grade update failed: {result}", status_code=response.status_code)
        return result

async def soft_delete_grade(data: dict, headers: dict):
    logger.info(f"Soft-deleting grade ID {data['id']}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?id=eq.{data['id']}",
                headers=headers,
                json={
                    "is_deleted": data["is_deleted"],
                    "updated_by": data["updated_by"],
                    "updated_at": current_timestamp()
                }
            )
            if response.status_code >= 400:
                result = response.json()
                raise GradeError(f"Grade deletion failed: {result}", status_code=response.status_code)
            return f"Grade deleted successfully"
    except GradeError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during deleting grade {data['grade_name']}")
        raise GradeError("Unexpected error", status_code=500)

async def fetch_active_grades(headers: dict):
    logger.info("Fetching active grades")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE}?is_deleted=eq.false&order=id.asc",
                headers=headers
            )
            result = response.json()
            if response.status_code >= 400:
                raise GradeError(f"Grade fetch failed: {result}", status_code=response.status_code)
            return result
    except GradeError as ue:
        raise ue
    except Exception:
        logger.exception(f"Unexpected error during fetching all grades")
        raise GradeError("Unexpected error", status_code=500)
