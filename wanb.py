import wandb as wandb


def end():
    wandb.finish()


def log(best, av):
    wandb.log({'best': best,
               'average': av})


class wanb:
    def __init__(self, name):
        wandb.init(project='ga', config={
            'name': name
        })
        wandb.run.name = name


if __name__ == '__main__':
    import time
    import random
    env = wanb(time.time())

    for x in range(1000):
        time.sleep(1)
        log(random.random(), random.randrange(1,10))

    end()
