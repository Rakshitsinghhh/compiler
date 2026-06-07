from src.optimizer.constant_fold import ConstantFolder


class Optimizer:

    def __init__(self):
        self.folder = ConstantFolder()

    def optimize(self, ast):
        """Run all optimization passes on the AST."""
        ast = self._fold_constants(ast)
        return ast

    def _fold_constants(self, node):
        return self.folder.optimize(node)
