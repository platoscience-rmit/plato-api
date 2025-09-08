from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

blogs_schema = extend_schema(
    summary="List blogs",
    description="Retrieve a list of blogs.",
    responses={
        200: OpenApiResponse(
            description="Success response",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value=[]
                )
            ]
        )
    },
    tags=["Blogs"]
)