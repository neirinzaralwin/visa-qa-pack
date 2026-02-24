def handler(request):
    return {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"status": "healthy", "message": "Railway function working"}'
    }
