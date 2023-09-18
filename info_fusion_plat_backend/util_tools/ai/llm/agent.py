from datetime import datetime
import logging
import uuid

from .thinking import Thinking

logger = logging.getLogger(__name__)

class Memory:
    pass

class AgentManager:
    """Agent管理类, 管理所有Agents
    """
    def __init__(
            self,
            default_thinking_type=Thinking.types.DEFAULT
        ):
        # 默认思考方式
        self.default_thinking_type = default_thinking_type
        
        # Agent历史记录
        self.history = []

    def do_init(self):
        # 全局主agent，所有agent都是这个agent的子agent
        self.global_main_agent = ManagerAgent(
            global_main_agent=True,
            thinking_type=self.default_thinking_type,
            one_time=False,
            source='生命周期管理器',
            agent_name='全局主Agent',
            agent_role='manager',
        )

    def add_history(self, content, operator, level="info", **kwargs):
        self.history.append(
            {
                "id": uuid.uuid4(),
                "content": content,
                "operator": operator,
                "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                "level" : level,
                **kwargs
            }
        )


class Agent:
    init_prompt = None

    def __init__(
            self,
            global_main_agent=False,
            parent_agent=None,
            thinking_type=Thinking.types.DEFAULT, 
            memory=None,
            one_time=False,
            source=None,
            agent_name=None,
            agent_role=None,
        ):

        # agent_id
        self.agent_id = uuid.uuid4()

        # 是否为全局主agent
        self.global_main_agent = global_main_agent

        # 父agent，每个agent最多只能对应一个
        self.parent_agent = parent_agent
        
        # 子agent，每个agent可以拥有多个子agent
        self.child_agents = {}

        # 思考方式(对应语言模型接口)
        self.thinking = Thinking(thinking_type=thinking_type)

        # agent的回忆，由多轮对话产生，也可以在初始化时手动构造
        self.memory = memory if memory else {"memory": []}

        # 是否一次性使用，设置为true时，在进行一次thinking后立即销毁,只能在作为子agent时设置为true
        self.one_time = one_time if parent_agent else False

        # agent使用的总token数
        self.total_tokens = 0

        # agent思考次数
        self.thinking_count = 0

        # agnet创建时间
        self.create_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        # 来源(创建者)
        self.source = source or "未知来源"

        # agent的角色，分为manager/worker/planner, 默认为worker
        self.agent_role = agent_role

        # agent的名称
        self.agent_name = agent_name or "未命名Agent"

        # agent的状态
        self.status = 'wait for init'

        # agent历史信息
        self.history = []

        self.add_history(
            content="创建完成",
            operator=self.source,
        )


    def add_history(self, content, operator, level="info", no_report=False, **kwargs):
        """新增历史记录

        Args:
            content (str): 历史记录内容
            operator (str): 操作者
            no_report (bool, optional): 是否向agent_manager汇报记录. Defaults to False.
        """
        self.history.append(
            {
                "id": uuid.uuid4(),
                "content": content,
                "operator": operator,
                "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                "level": level,
                **kwargs
            }
        )
        if not no_report:
            agent_manager.add_history(
                content = f"{self.agent_name} 创建完成",
                operator = operator,
                agent_id = self.agent_id,
                level=level,
                kwargs=kwargs
            )

class ManagerAgent(Agent):
    def __init__(
            self, 
            global_main_agent=False,
            parent_agent=None,
            thinking_type=Thinking.types.DEFAULT, 
            memory=None,
            one_time=False,
            source=None,
            agent_name=None,
            agent_role='manager',
        ):
        super().__init__(
            global_main_agent=global_main_agent,
            parent_agent=parent_agent,
            thinking_type=thinking_type, 
            memory=memory,
            one_time=one_time,
            source=source,
            agent_name=agent_name,
            agent_role=agent_role,
        )

class WorkerAgent(Agent):
    def __init__(
            self, 
            global_main_agent=False,
            parent_agent=None,
            thinking_type=Thinking.types.DEFAULT, 
            memory=None,
            one_time=False,
            source=None,
            agent_name=None,
            agent_role='worker',
            **kwargs
        ):
        super().__init__(
            global_main_agent=global_main_agent,
            parent_agent=parent_agent,
            thinking_type=thinking_type, 
            memory=memory,
            one_time=one_time,
            source=source,
            agent_name=agent_name,
            agent_role=agent_role,
        )

class PlannerAgent(Agent):
    def __init__(
            self, 
            global_main_agent=False,
            parent_agent=None,
            thinking_type=Thinking.types.DEFAULT, 
            memory=None,
            one_time=False,
            source=None,
            agent_name=None,
            agent_role='planner',
            **kwargs
        ):
        super().__init__(
            global_main_agent=global_main_agent,
            parent_agent=parent_agent,
            thinking_type=thinking_type, 
            memory=memory,
            one_time=one_time,
            source=source,
            agent_name=agent_name,
            agent_role=agent_role,
        )


agent_manager = AgentManager()
agent_manager.do_init()
global_main_agent = agent_manager.global_main_agent
