"""开通sysom MCP Helper实现

负责开通sysom MCP工具逻辑
"""
from typing import Dict, Any, Optional, TYPE_CHECKING
from pydantic import BaseModel, Field
from .logger_config import setup_logger
from .mcp_helper import MCPHelper, MCPRequest, MCPResponse

logger = setup_logger(__name__)
from .openapi_client import OpenAPIClient, AlibabaCloudSDKClient
from .api_registry import APIRegistry
from alibabacloud_sysom20231230 import models as sysom_20231230_models
from Tea.model import TeaModel

class InitialResultCode:
    """初始化结果状态码常量"""
    SUCCESS = "Success"
    ERROR = "Error"

class InitialSysomMCPHelper(MCPHelper):
    """开通sysom MCP Helper实现"""
    async def initial_sysom(
        self,
        check_only: bool = False,
    ) -> MCPResponse:
        """
        开通sysom MCP工具
        """
        
        api_name = "initial_sysom"
        
        # 注册路由（如果尚未注册）
        registry = APIRegistry()
        if registry.get_route(api_name) is None:

            # 注册SDK路由
            registry.register_sdk(
                api_name=api_name,
                request_model=sysom_20231230_models.InitialSysomRequest,
                response_model=sysom_20231230_models.InitialSysomResponse,
                client_method=lambda client, req: client.initial_sysom_async(req)
            )
        # SDK调用：传入TeaModel
        initial_request = sysom_20231230_models.InitialSysomRequest(
            check_only= check_only,
            source = "mcp"
        )
        # 调用initial_sysom接口
        success, response_data, error_msg = await self.client.call_api(
            api_name=api_name,
            request=initial_request
        )
        if not success:
            return MCPResponse(
                code=InitialResultCode.ERROR,
                message=error_msg or "开通sysom失败，请前往https://alinux.console.aliyun.com进行开通",
                data=None
            )
        return MCPResponse(
            code=InitialResultCode.SUCCESS,
            message="initial sysom调用成功",
            data=response_data
        )
    
    