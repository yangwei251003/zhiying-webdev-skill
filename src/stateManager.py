"""
状态管理器 —— 维护六阶段状态机，执行状态流转规则

状态流转:
    requirement_analysis → product_design → tech_design → development → testing → deployment
    任意阶段 → requirement_analysis（重新设计需求时）
    product_design → tech_design（设计完成后）
    tech_design → development（架构完成后）
    development → testing（开发完成后）
    testing → deployment（测试通过后）
"""

from typing import Optional
import json


class StateManager:
    """六阶段状态机管理器"""

    VALID_STAGES = [
        "requirement_analysis",
        "product_design",
        "tech_design",
        "development",
        "testing",
        "deployment",
    ]

    def __init__(self):
        self._stage = "requirement_analysis"
        self._requirement_loaded = False
        self._design_loaded = False
        self._tech_loaded = False
        self._development_complete = False
        self._test_passed = False
        self._deployment_complete = False

    def get_stage(self) -> str:
        """获取当前阶段"""
        return self._stage

    def set_stage(self, stage: str) -> None:
        """手动设置阶段（需验证合法性）"""
        if stage not in self.VALID_STAGES:
            raise ValueError(f"无效阶段: {stage}，有效值: {self.VALID_STAGES}")
        self._stage = stage

    def set_requirement_loaded(self) -> None:
        """标记需求已加载"""
        self._requirement_loaded = True
        if self._requirement_loaded:
            if self._design_loaded:
                self._stage = "tech_design"
            else:
                self._stage = "product_design"

    def set_design_loaded(self) -> None:
        """标记设计已加载"""
        self._design_loaded = True
        if self._requirement_loaded and self._design_loaded:
            self._stage = "tech_design"

    def can_advance(self) -> bool:
        """判断当前阶段是否可以推进"""
        if self._stage == "requirement_analysis":
            return self._requirement_loaded
        elif self._stage == "product_design":
            return self._design_loaded
        elif self._stage == "tech_design":
            return self._tech_loaded
        elif self._stage == "development":
            return self._development_complete
        elif self._stage == "testing":
            return self._test_passed
        elif self._stage == "deployment":
            return False  # 已到达终点
        return False

    def advance(self) -> Optional[str]:
        """推进到下一阶段，返回新阶段名"""
        order = self.VALID_STAGES
        current_idx = order.index(self._stage)
        if current_idx < len(order) - 1:
            self._stage = order[current_idx + 1]
            return self._stage
        return None

    def force_advance(self, target_stage: str) -> str:
        """强制跳转到指定阶段（用于降级例外）"""
        if target_stage not in self.VALID_STAGES:
            raise ValueError(f"无效阶段: {target_stage}")
        self._stage = target_stage
        return self._stage

    def rollback_to_requirement(self) -> str:
        """回退到需求分析阶段（用户重新设计需求时）"""
        self._stage = "requirement_analysis"
        self._design_loaded = False
        self._tech_loaded = False
        self._development_complete = False
        self._test_passed = False
        self._deployment_complete = False
        return self._stage

    def rollback_to_design(self) -> str:
        """回退到产品设计阶段（用户修改设计时）"""
        self._stage = "product_design"
        self._tech_loaded = False
        self._development_complete = False
        self._test_passed = False
        self._deployment_complete = False
        return self._stage

    def rollback_to_development(self) -> str:
        """回退到开发阶段（用户修改代码时）"""
        self._stage = "development"
        self._test_passed = False
        self._deployment_complete = False
        return self._stage

    def set_design_complete(self) -> None:
        """设置设计完成"""
        self._design_loaded = True
        self._stage = "tech_design"

    def set_tech_complete(self) -> None:
        """设置技术架构完成"""
        self._tech_loaded = True
        self._stage = "development"

    def set_development_complete(self) -> None:
        """设置开发完成"""
        self._development_complete = True
        self._stage = "testing"

    def set_test_complete(self) -> None:
        """设置测试完成"""
        self._test_passed = True
        self._stage = "deployment"

    def set_deployment_complete(self) -> None:
        """设置部署完成"""
        self._deployment_complete = True
        print("[演示] 🎉 演示状态已到达部署阶段；未执行真实部署。")

    def is_degraded_mode(self) -> bool:
        """判断是否处于降级模式（跳过了阶段）"""
        order = self.VALID_STAGES
        current_idx = order.index(self._stage)
        # 如果在 deployment 但前面的阶段未完成 = 降级模式
        if self._stage == "deployment":
            return not (
                self._requirement_loaded
                and self._design_loaded
                and self._tech_loaded
                and self._development_complete
                and self._test_passed
            )
        return False

    def get_missing_requirements(self) -> list:
        """获取缺失的需求项"""
        missing = []
        if not self._requirement_loaded:
            missing.append("需求文档未完整")
        if not self._design_loaded:
            missing.append("设计稿未完整")
        if not self._tech_loaded:
            missing.append("技术架构未完整")
        return missing

    def to_dict(self) -> dict:
        """导出状态字典"""
        return {
            "stage": self._stage,
            "requirement_loaded": self._requirement_loaded,
            "design_loaded": self._design_loaded,
            "tech_loaded": self._tech_loaded,
            "development_complete": self._development_complete,
            "test_passed": self._test_passed,
            "deployment_complete": self._deployment_complete,
        }

    def from_dict(self, state: dict) -> None:
        """从字典恢复状态"""
        self._stage = state.get("stage", "requirement_analysis")
        self._requirement_loaded = state.get("requirement_loaded", False)
        self._design_loaded = state.get("design_loaded", False)
        self._tech_loaded = state.get("tech_loaded", False)
        self._development_complete = state.get("development_complete", False)
        self._test_passed = state.get("test_passed", False)
        self._deployment_complete = state.get("deployment_complete", False)