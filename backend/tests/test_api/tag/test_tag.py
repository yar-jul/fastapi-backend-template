from fastapi import FastAPI, status
from httpx import AsyncClient


async def test_tag(
    app: FastAPI,
    client: AsyncClient,
    tag_1: dict,
) -> None:
    post_response = await client.post(app.url_path_for("tag:post_tag"), json=tag_1)
    assert post_response.status_code == status.HTTP_200_OK
    get_drones_response = await client.get(app.url_path_for("tag:post_tag"))
    assert get_drones_response.status_code == status.HTTP_200_OK
