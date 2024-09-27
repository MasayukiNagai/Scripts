import time
import sys


def execute_job(job_id):
    time.sleep(5)
    msg = f"executed {job_id}th job"
    print(msg)
    with open(f"./test_output_{job_id}.txt", "w") as f:
        f.write(msg)


def execute_job_screen(screen_id, job_id, ):
    time.sleep(5)
    msg = f"executed {job_id}th job on screen {screen_id}"
    print(msg)
    with open(f"./test_output_{job_id}.txt", "w") as f:
        f.write(msg)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        job_id = sys.argv[1]
        execute_job(job_id)
    elif len(sys.argv) == 3:
        screen_id = sys.argv[1]
        job_id = sys.argv[2]
        execute_job_screen(screen_id, job_id)
    else:
        msg = "Usage: python test.py <job_id> or python test.py <screen_id> <job_id>"
        sys.exit(msg)
