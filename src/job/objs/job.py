from datetime import timedelta


class Job:
    def __init__(
        self,
        uuid_job_id,
        slurm_job_id=None,
        status=None,
        url=None,
        port=None,
        host=None,
        running_time=timedelta(seconds=0),
    ):
        self.uuid_job_id = uuid_job_id
        self.slurm_job_id = slurm_job_id
        self.status = status
        self.url = url
        self.port = port
        self.host = host
        self.running_time = running_time

    def __repr__(self):
        return f"Job(uuid={self.uuid_job_id}, slurm_id={self.slurm_job_id}, status={self.status}, running_time={self.running_time}, url={self.url}, host={self.host}, port={self.port})"

    def to_dict(self):
        return {
            "uuid_job_id": self.uuid_job_id,
            "slurm_job_id": self.slurm_job_id,
            "status": self.status,
            "url": self.url,
            "port": self.port,
            "host": self.host,
            "running_time": str(self.running_time),
        }
