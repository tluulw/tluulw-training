from data import db_session
from data.jobs import Jobs
from data.users import User


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()

    jobs = []

    for job in db_sess.query(Jobs).all():
        if jobs:
            if len(job.collaborators) == len(jobs[-1].collaborators):
                jobs.append(job)
            elif len(job.collaborators) > len(jobs[-1].collaborators):
                jobs.clear()
                jobs.append(job)
        else:
            jobs.append(job)

    for job in jobs:
        for team_leader in db_sess.query(User).filter(User.id.like(job.team_leader)).all():
            print(team_leader.surname, team_leader.name)


if __name__ == '__main__':
    main()