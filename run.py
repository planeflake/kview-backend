import uvicorn
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run the FastAPI application')
    parser.add_argument('--env', type=str, default='dev', choices=['dev', 'prod'],
                       help='Environment to run the app in')
    args = parser.parse_args()

    if args.env == 'dev':
        uvicorn.run(
            "app:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="debug"
        )
    else:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",  # Allow external connections in prod
            port=8000,
            workers=4,       # Multiple workers for production
            log_level="info"
        )

if __name__ == "__main__":
    main()