from config import get_settings

def main():
    settings = get_settings()
    print(settings.urls)
    print(settings.retry_attempts)
    print(settings.timeout_seconds)

if __name__ == "__main__":
    main()
