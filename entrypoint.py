from home_task.cli import CLI
import argparse
from fastapi import FastAPI
import uvicorn
from home_task.backend import get_statistics

app = FastAPI()
app.include_router(get_statistics.router)


def main():
    parser = argparse.ArgumentParser(
                        prog='Calculate Days to Hire',
                        description='Calculate the number of days to hire a candidate')

    parser.add_argument('-d', '--days_to_hire', action='store_true')
    parser.add_argument('-t', '--threshold', type=int, help='Threshold for job postings frequency')

    args = parser.parse_args()
    
    if args.days_to_hire:
        threshold = 5
        if args.threshold:
            threshold = int(args.threshold)

        print(f"Threshold: {threshold}")    
        cli = CLI(threshold=threshold)
        cli.start_flow()

    else:
        uvicorn.run(
        "entrypoint:app",       
        host="127.0.0.1",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()