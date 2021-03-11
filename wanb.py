import wandb as wandb


# this is just a few functions to manage the 'Weights and Bias' service in the back round
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


# test script
if __name__ == '__main__':
    import time
    import random
    env = wanb(time.time())

    for x in range(1000):
        time.sleep(1)
        log(random.random(), random.randrange(1,10))

    end()
