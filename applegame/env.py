import numpy as np

from applegame.action_map import ActionMap
from applegame.board import Board

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError as exc:
    raise ImportError(
        "gymnasium is required for AppleGameEnv. Install with: pip install gymnasium"
    ) from exc


class AppleGameEnv(gym.Env):
    metadata = {"render_modes": ["ansi"]}

    def __init__(
        self,
        rows=10,
        cols=17,
        invalid_action_penalty=-0.1,
        max_steps=None,
        seed=None,
    ):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.invalid_action_penalty = float(invalid_action_penalty)
        self.max_steps = max_steps
        self.action_map = ActionMap(rows, cols)
        self.action_space = spaces.Discrete(self.action_map.size)
        self.observation_space = spaces.Box(
            low=0, high=9, shape=(rows, cols), dtype=np.int8
        )
        self.board = Board(rows, cols)
        self.np_random = np.random.default_rng(seed)
        self.step_count = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        if seed is not None:
            self.np_random = np.random.default_rng(seed)
        self.board.randomize(self.np_random)
        self.step_count = 0
        mask = self.board.valid_action_mask(self.action_map)
        info = {"action_mask": mask}
        return self.board.values.copy(), info

    def step(self, action):
        r1, c1, r2, c2 = self.action_map.decode(int(action))
        valid, removed = self.board.apply_rect(r1, c1, r2, c2)
        if valid:
            reward = float(removed)
        else:
            reward = float(self.invalid_action_penalty)
        self.step_count += 1

        mask = self.board.valid_action_mask(self.action_map)
        terminated = not mask.any()
        truncated = False
        if self.max_steps is not None and self.step_count >= self.max_steps:
            truncated = True

        info = {"action_mask": mask, "is_valid": valid}
        return self.board.values.copy(), reward, terminated, truncated, info

    def get_action_mask(self):
        return self.board.valid_action_mask(self.action_map)

    def render(self):
        lines = []
        for row in self.board.values:
            lines.append(" ".join(str(int(v)) for v in row))
        return "\n".join(lines)
