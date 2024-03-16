from data import db_session
from data.jobs import Jobs
from data.users import User


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()

    jobs = []
    team_leaders = set()

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
            team_leaders.add((team_leader.name, team_leader.surname))

    for elem in team_leaders:
        print(*elem)


if __name__ == '__main__':
    main()