"""
ZhiYing WebDev —— 职映网站全流程开发智能体
主入口模块

用法:
    python index.py --mode interactive
    python index.py --requirement <requirement.md> --design <design.md>
    python index.py --stage <stage_name>
"""

import json
import os
import sys
import argparse
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from stateManager import StateManager


class ZhiYingWebDev:
    """ZhiYing WebDev 主控制器 —— 协调各模块按状态机流转"""

    def __init__(self, requirement_path=None, design_path=None):
        self.state_manager = StateManager()

        # Load existing requirement if provided
        self.requirement = None
        self.design = None
        self.tech_architecture = None
        self.code = None
        self.test_result = None

        if requirement_path:
            with open(requirement_path, "r", encoding="utf-8") as f:
                self.requirement = f.read()
            self.state_manager.set_requirement_loaded()

        if design_path and self.requirement:
            with open(design_path, "r", encoding="utf-8") as f:
                self.design = f.read()
            self.state_manager.set_design_loaded()

    def run_interactive(self):
        """交互式运行模式"""
        print("=" * 60)
        print("  🎯 ZhiYing WebDev —— 职映网站全流程开发智能体")
        print("=" * 60)
        print()
        print("我会引导你完成六个阶段：")
        print("  ① 需求分析 → ② 产品设计 → ③ 技术设计 → ④ 开发实现 → ⑤ 测试优化 → ⑥ 部署上线")
        print()
        print("随时输入 /help 查看命令，/quit 退出，/skip 阶段")
        print("-" * 60)

        while True:
            stage = self.state_manager.get_stage()
            prompt = self._get_stage_prompt(stage)
            user_input = input(f"\n[{stage.upper()}] {prompt}\n> ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                self._handle_command(user_input)
                continue

            # Route to appropriate stage handler
            self._handle_stage_input(stage, user_input)

            # Check if we can advance
            if self.state_manager.can_advance():
                self.state_manager.advance()

    def _get_stage_prompt(self, stage):
        prompts = {
            "requirement_analysis": "请描述你的网站需求（从项目背景开始），或输入 /skip 先出基础版网站：",
            "product_design": "需求分析完成！正在进行产品设计...\n输入 /design 开始设计，或上传设计稿：",
            "tech_design": "设计完成！请确认设计方案，或输入 /tech 开始技术架构设计：",
            "development": "技术架构完成！输入 /develop 开始开发：",
            "testing": "开发完成！输入 /test 开始测试：",
            "deployment": "测试通过！输入 /deploy 开始部署：",
        }
        return prompts.get(stage, "请输入：")

    def _handle_command(self, cmd):
        if cmd == "/quit":
            print("👋 再见！随时回来继续开发网站～")
            sys.exit(0)
        elif cmd == "/help":
            self._print_help()
        elif cmd == "/skip":
            if self.state_manager.get_stage() == "requirement_analysis":
                print("⚠️  降级模式：将基于当前已收集的需求生成基础版网站")
                print("以下功能因需求不明确而影响质量：")
                missing = self.state_manager.get_missing_requirements()
                for m in missing:
                    print(f"  - {m}")
                self.state_manager.force_advance("development")
        elif cmd == "/design":
            if self.state_manager.get_stage() == "product_design":
                self._run_product_design()
        elif cmd == "/tech":
            if self.state_manager.get_stage() == "tech_design":
                self._run_tech_design()
        elif cmd == "/develop":
            if self.state_manager.get_stage() == "development":
                self._run_development()
        elif cmd == "/test":
            if self.state_manager.get_stage() == "testing":
                self._run_testing()
        elif cmd == "/deploy":
            if self.state_manager.get_stage() == "deployment":
                self._run_deployment()
        elif cmd == "/status":
            self._print_status()

    def _handle_stage_input(self, stage, user_input):
        if stage == "requirement_analysis":
            # 这里应该调用需求分析器处理用户输入
            print(f"\n收到需求描述：{user_input[:50]}...")
            print("[演示] 正在分析需求...")
        elif stage == "product_design":
            # 这里应该调用产品设计器处理用户输入
            print(f"\n收到设计反馈：{user_input[:50]}...")
        elif stage == "tech_design":
            # 这里应该调用技术架构师处理用户输入
            print(f"\n收到技术反馈：{user_input[:50]}...")
        elif stage == "development":
            self._run_development()
        elif stage == "testing":
            self._run_testing()
        elif stage == "deployment":
            self._run_deployment()

    def _run_product_design(self):
        print("\n🎨 开始产品设计...")
        print("[演示] 正在设计首页Hero区域...")
        print("[演示] 正在设计页面布局...")
        print("[演示] 正在设计功能模块...")
        print("[演示] 正在生成图片资源...")
        print("[演示] \n✅ 产品设计完成！")
        print("[演示] 产出物：")
        print("  - 完整设计稿")
        print("  - 视觉规范文档")
        print("  - 图片资源文件")
        self.state_manager.set_design_complete()

    def _run_tech_design(self):
        print("\n🏗️ 开始技术架构设计...")
        print("[演示] 正在设计前端技术选型...")
        print("[演示] 正在设计后端技术选型...")
        print("[演示] 正在设计部署架构...")
        print("[演示] 正在编写接口文档...")
        print("[演示] 正在制定开发计划...")
        print("[演示] \n✅ 技术架构设计完成！")
        print("[演示] 产出物：")
        print("  - 技术架构方案")
        print("  - 接口文档")
        print("  - 开发计划书")
        self.state_manager.set_tech_complete()

    def _run_development(self):
        print("\n💻 开始开发实现...")
        print("[演示] 正在开发前端页面...")
        print("[演示] 正在开发前端组件...")
        print("[演示] 正在实现动画效果...")
        print("[演示] 正在开发后端接口...")
        print("[演示] 正在生成图片资源...")
        print("[演示] \n✅ 开发完成！")
        print("[演示] 产出物：")
        print("  - 前端代码（HTML/CSS/JS）")
        print("  - 后端代码（如果需要）")
        print("  - 图片资源文件")
        self.state_manager.set_development_complete()

    def _run_testing(self):
        print("\n🔍 开始测试优化...")
        print("[演示] 正在执行页面设计还原检查...")
        print("[演示] 正在执行功能实现检查...")
        print("[演示] 正在执行交互流畅性检查...")
        print("[演示] 正在执行动画流畅性检查...")
        print("[演示] 正在执行响应式布局检查...")
        print("[演示] 正在执行性能达标检查...")
        print("[演示] 正在执行用户体验检查...")
        print("[演示] 正在执行视觉质量检查...")
        print("[演示] 正在执行代码质量检查...")
        print("[演示] \n✅ 测试通过！")
        print("[演示] 产出物：")
        print("  - 测试报告")
        print("  - 优化建议")
        self.state_manager.set_test_complete()

    def _run_deployment(self):
        print("\n🚀 开始部署上线...")
        print("[演示] 正在打包和优化代码...")
        print("[演示] 正在配置环境...")
        print("[演示] 正在部署数据库...")
        print("[演示] 正在配置域名和SSL证书...")
        print("[演示] 正在配置CDN...")
        print("[演示] 正在编写文档...")
        print("[演示] 正在执行上线检查...")
        print("[演示] \n✅ 演示部署阶段完成；没有网站被上传。")
        print("[演示] 产出物：")
        print("  - 开发文档")
        print("  - 测试文档")
        print("  - 运维手册")
        print("  - 用户使用说明书")
        self.state_manager.set_deployment_complete()

    def _print_help(self):
        print("""
命令列表：
  /help    - 显示帮助
  /quit    - 退出
  /skip    - 跳过当前阶段，先生成基础版网站
  /design  - 开始产品设计
  /tech    - 开始技术架构设计
  /develop - 开始开发实现
  /test    - 开始测试优化
  /deploy  - 开始部署上线
  /status  - 查看当前进度

阶段说明：
  requirement_analysis - 需求分析与头脑风暴
  product_design       - UI/UX产品设计
  tech_design          - 技术架构设计
  development          - 开发实现
  testing              - 测试优化
  deployment           - 部署上线
        """)

    def _print_status(self):
        stage = self.state_manager.get_stage()
        progress = {
            "requirement_analysis": "📝 阶段一：需求分析（16%）",
            "product_design": "🎨 阶段二：产品设计（33%）",
            "tech_design": "🏗️ 阶段三：技术设计（50%）",
            "development": "💻 阶段四：开发实现（66%）",
            "testing": "🔍 阶段五：测试优化（83%）",
            "deployment": "🚀 阶段六：部署上线（100%）",
        }
        print(f"\n当前阶段：{progress.get(stage, stage)}")


def main():
    print("[WIP演示] 本CLI只展示阶段和状态，尚未接入代码生成、测试或部署服务。")
    parser = argparse.ArgumentParser(
        description="ZhiYing WebDev —— 职映网站全流程开发智能体"
    )
    parser.add_argument(
        "--mode",
        choices=["interactive", "batch"],
        default="interactive",
        help="运行模式：interactive（交互式）/ batch（批量处理）",
    )
    parser.add_argument("--requirement", help="需求文档文件路径")
    parser.add_argument("--design", help="设计文档文件路径")
    parser.add_argument("--stage", help="从指定阶段开始")
    parser.add_argument("--output", default="./output", help="输出目录")

    args = parser.parse_args()

    app = ZhiYingWebDev(requirement_path=args.requirement, design_path=args.design)

    if args.mode == "interactive":
        app.run_interactive()
    elif args.mode == "batch":
        if not args.requirement or not args.design:
            print("❌ 批量模式需要 --requirement 和 --design 参数")
            sys.exit(1)
        # Batch mode: direct generation
        app._run_tech_design()
        app._run_development()
        app._run_testing()
        app._run_deployment()


if __name__ == "__main__":
    main()