from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.wrappers import ActionMasker

from applegame.env import AppleGameEnv


def mask_fn(env):
    return env.get_action_mask()


def main():
    env = AppleGameEnv()
    env = ActionMasker(env, mask_fn)

    model = MaskablePPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=200_000)
    model.save("applegame_maskable_ppo")


if __name__ == "__main__":
    main()
