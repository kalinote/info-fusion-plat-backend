from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class Thinking:
    """Agent的思考方式
    """

    def __init__(
            self,
            thinking_type
        ):
        self.thinking_type = thinking_type

    class types:
        OPENAI_GPT3 = 'openai_gpt3'
        DEFAULT = OPENAI_GPT3

class AgentManager:
    """Agent管理类, 管理所有Agents
    """
    def __init__(
            self,
            default_thinking_type=Thinking.types.DEFAULT
        ):

        # 全局主agent，所有agent都是这个agent的子agent
        self.global_main_agent = ManagerAgent(
            global_main_agent=True,
            thinking_type=default_thinking_type,
            one_time=False,
            agent_role='manager'
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
            agent_role=None
        ):

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
        self.create_time = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

        # agent的角色，分为manager/worker/planner, 默认为worker
        self.agent_role= agent_role

        # agent的状态
        self.status = 'wait for init'


class ManagerAgent(Agent):
    def __init__(
            self, 
            global_main_agent=False, 
            parent_agent=None, 
            thinking_type=Thinking.types.DEFAULT, 
            memory=None, 
            one_time=False, 
            agent_role='manager'
        ):
        super().__init__(
            global_main_agent, 
            parent_agent, 
            thinking_type, 
            memory, 
            one_time, 
            agent_role
        )

class WorkerAgent(Agent):
    def __init__(
            self, 
            parent_agent=None, 
            thinking_type=Thinking.types.DEFAULT, 
            memory=None, 
            one_time=False, 
            agent_role='worker'
        ):
        super().__init__(
            parent_agent, 
            thinking_type, 
            memory, 
            one_time, 
            agent_role
        )

class PlannerAgent(Agent):
    def __init__(
            self, 
            parent_agent=None, 
            thinking_type=Thinking.types.DEFAULT, 
            memory=None, 
            one_time=False, 
            agent_role='planner'
        ):
        super().__init__(
            parent_agent, 
            thinking_type, 
            memory, 
            one_time, 
            agent_role
        )


agent_manager = AgentManager()
