import subprocess
import os
from typing import List
from datetime import timedelta
from river.objects import Job


def get_slurm_jobs(jobs: List[Job]):
    river_home = os.getenv("RIVER_HOME")
    if not river_home:
        raise EnvironmentError("RIVER_HOME environment variable is not set")
    for job in jobs:
        job_path = f"{river_home}/.river/jobs/{job.uuid_job_id}"
        if not os.path.exists(job_path):
            job.status = "NOT_FOUND"
        if os.path.exists(f"{job_path}/job.proxy_location"):
            proxy_location = subprocess.check_output(
                f"cat {job_path}/job.proxy_location", shell=True
            )
            job.proxy_location = proxy_location.decode().strip()
        if os.path.exists(f"{job_path}/job.id"):
            slurm_id = subprocess.check_output(f"cat {job_path}/job.id", shell=True)
            job.slurm_job_id = slurm_id.decode().strip()
        if os.path.exists(f"{job_path}/job.url"):
            slurm_url = subprocess.check_output(f"cat {job_path}/job.url", shell=True)
            job.url = slurm_url.decode().strip()
        if os.path.exists(f"{job_path}/job.port"):
            slurm_port = subprocess.check_output(f"cat {job_path}/job.port", shell=True)
            job.port = slurm_port.decode().strip()
        if os.path.exists(f"{job_path}/job.host"):
            slurm_host = subprocess.check_output(f"cat {job_path}/job.host", shell=True)
            job.host = slurm_host.decode().strip()


def parse_duration(duration_str):
    if "-" in duration_str:
        days, time = duration_str.split("-")
        total_seconds = 0
        if days:
            total_seconds += int(days) * 24 * 3600
        hours, minutes, seconds = map(int, time.split(":"))
        total_seconds += hours * 3600 + minutes * 60 + seconds
    elif ":" in duration_str:
        parts = duration_str.split(":")
        if len(parts) == 2:
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError(f"Invalid duration format: {duration_str}")
    else:
        total_seconds = int(duration_str)
    return timedelta(seconds=total_seconds)


def parsing_squeue_status(jobs: List[Job], states: str):
    if states:
        lines = states.split("\n")[1:-1]
        for line in lines:
            for job in jobs:
                if job.slurm_job_id == line.split()[0]:
                    job_id, state, time = line.split()
                    job.running_time = parse_duration(time)
                    job.status = state


def get_jobs_info(jobs: List[Job]):
    get_slurm_jobs(jobs)
    job_ids = [job.slurm_job_id for job in jobs if job.slurm_job_id]
    if not job_ids:
        return

    job_ids_str = ",".join(job_ids)
    commands = [
        f"squeue --jobs {job_ids_str} --format='%.18i %.9T %.10M'",
        f"sacct --jobs {job_ids_str} --format='JobID,State,Elapsed'",
    ]

    job_info = None
    for cmd in commands:
        try:
            job_info = subprocess.check_output(
                cmd, shell=True, stderr=subprocess.DEVNULL
            ).decode("utf-8")
            if job_info:
                break
        except subprocess.CalledProcessError:
            continue

    if job_info:
        parsing_squeue_status(jobs, job_info)
