responses = {
    "test_response": {
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            'key1': 'value1',
                            'key2': True,
                            'key3': 1,
                        }
                    }
                }
            }
        }
    }
}
