import wandb as wandb


# this is just a few functions to manage the 'Weights and Bias' service in the back round
class wanb:
    def __init__(self, name, startingStep):
        self.step = startingStep
        wandb.init(project='ga', config={
            'name': name
        })
        wandb.run.name = name

    def log(self, best, av):
        wandb.log({'best': best,
                   'average': av}, self.step)
        self.step += 1

    def end(self):
        wandb.finish()

# test script
if __name__ == '__main__':
    import time
    import random
    env = wanb(time.time())

    for x in range(1000):
        time.sleep(1)
        env.log(random.random(), random.randrange(1,10))

    env.end()
