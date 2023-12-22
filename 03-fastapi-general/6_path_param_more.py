import uvicorn
from fastapi import FastAPI, Query, Path

app = FastAPI()


# 'Path' 함수를 추가해서 'title' 이라는 메타데이터 추가. Query param 방식이랑 같다.
# @app.get("/items/{item_id}")
# async def read_items(item_id: int = Path(..., title="아이템 식별을 위한 ID "),
#                      q: str | None = Query(None, alias="item-query")):
#     # request 한 item_id 를 반환한다.
#     # q 가 존재하면 {"q": q} 를 추가한다.
#
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# 숫자제한이 가능하다.
# - ge: greater than or equal (크거나 같다)
# - gt: greater than (크다)
# - le: less than or equal (작거나 같다)
# - lt: less than (작다)
@app.get("/items/{item_id}")
async def read_items(item_id: int = Path(..., title="아이템 식별을 위한 ID ", lt=5),
                     q: str | None = Query(None, alias="item-query")):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


if __name__ == "__main__":
    uvicorn.run("6_path_param_more:app", host="localhost", port=8000, reload=True)
