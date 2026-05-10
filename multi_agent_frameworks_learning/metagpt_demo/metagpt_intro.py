"""
MetaGPT 入门项目：模拟软件公司运作
======================================
核心概念：
- Role: 公司中的职位角色（产品经理、架构师、工程师、测试等）
- Action: 角色执行的具体动作
- Environment: 公司环境，角色在其中协作
- Message: 角色间通信的消息对象
- SOP: 标准作业流程，定义工作流

本示例模拟一个软件公司的完整开发流程：
1. 📋 ProductManager（产品经理）：需求分析和PRD撰写
2. 🏗️ Architect（架构师）：技术设计和系统设计
3. 👨‍💻 Engineer（工程师）：代码实现
4. 🧪 QaEngineer（测试工程师）：测试用例和测试执行
"""

import asyncio
import re
from metagpt.roles import Role
from metagpt.actions import Action
from metagpt.schema import Message
from metagpt.environment import Environment
from metagpt.team import Team
from metagpt.logs import logger


# ============================================================
# 1. 自定义 Action（动作）
# ============================================================

class WritePRD(Action):
    """
    动作：撰写产品需求文档（PRD）
    执行者：产品经理
    """
    
    name = "WritePRD"
    
    async def run(self, requirement: str) -> str:
        """执行PRD撰写动作"""
        
        prd_content = f"""
# 产品需求文档（PRD）

## 1. 项目概述
**项目名称**: 智能任务管理系统
**版本**: v1.0
**日期**: 2024年
**作者**: 产品经理

### 1.1 项目背景
{requirement}

### 1.2 项目目标
构建一个高效、易用的任务管理系统，帮助团队更好地协作和管理工作任务。

---

## 2. 用户故事

### US-001: 任务创建
**作为** 团队成员  
**我希望** 能够快速创建新任务  
**以便** 追踪和管理我的工作  

**验收标准**:
- [ ] 可以设置任务标题、描述、优先级
- [ ] 可以指定截止日期和负责人
- [ ] 可以添加标签和分类

### US-002: 任务列表查看
**作为** 团队成员  
**我希望** 能够按不同条件筛选和排序任务  
**以便** 快速找到我关注的任务  

**验收标准**:
- [ ] 支持按状态、优先级、负责人筛选
- [ ] 支持按截止日期、创建时间排序
- [ ] 支持看板视图和列表视图切换

### US-003: 任务状态更新
**作为** 团队成员  
**我希望** 能够更新任务状态（待办/进行中/已完成）  
**以便** 团队了解项目进展  

**验收标准**:
- [ ] 状态变更时自动记录时间戳
- [ ] 状态变更时通知相关人员
- [ ] 支持批量更新状态

### US-004: 协作评论
**作为** 团队成员  
**我希望** 能够在任务下添加评论和附件  
**以便** 与团队成员沟通任务细节  

**验收标准**:
- [ ] 支持 @提及团队成员
- [ ] 支持上传文件附件
- [ ] 评论支持富文本格式

---

## 3. 功能需求

### 3.1 功能清单
| ID | 功能 | 优先级 | 复杂度 |
|----|------|--------|--------|
| F001 | 用户注册登录 | P0 | 中 |
| F002 | 任务CRUD | P0 | 低 |
| F003 | 任务筛选排序 | P1 | 中 |
| F004 | 看板视图 | P1 | 高 |
| F005 | 评论系统 | P2 | 中 |
| F006 | 通知提醒 | P2 | 高 |
| F007 | 数据统计 | P3 | 高 |
| F008 | 权限管理 | P1 | 高 |

### 3.2 非功能性需求
- **性能**: 页面加载时间 < 2秒，API响应时间 < 500ms
- **并发**: 支持100+用户同时在线
- **可用性**: 系统可用性 > 99.9%
- **安全性**: 数据加密传输，RBAC权限控制
- **可扩展性**: 微服务架构，支持水平扩展

---

## 4. UI/UX 要求
- 响应式设计，支持Web和移动端
- 界面简洁直观，学习成本低
- 符合无障碍访问标准（WCAG 2.1）

---

## 5. 验收标准
- [ ] 所有P0功能完整实现并通过测试
- [ ] 核心流程端到端测试通过
- [ ] 性能指标达标
- [ ] 安全审计通过
"""
        
        logger.info("✅ PRD文档已生成")
        return prd_content


class DesignArchitecture(Action):
    """
    动作：设计系统架构
    执行者：架构师
    """
    
    name = "DesignArchitecture"
    
    async def run(self, prd: str) -> str:
        """执行架构设计动作"""
        
        architecture_doc = f"""
# 系统架构设计文档

## 1. 架构概览

### 1.1 架构风格
采用前后端分离的微服务架构，具备高可用、可扩展特性。

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Web App  │  │ Mobile   │  │  API     │                  │
│  │ (React)  │  │ (Flutter)│  │  Client  │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
└───────┼─────────────┼─────────────┼─────────────────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                        网关层                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              API Gateway (Kong/Nginx)                │   │
│  │  • 路由转发  • 负载均衡  • 限流熔断  • 身份认证      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      服务层                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ 用户服务 │ │ 任务服务 │ │ 通知服务 │ │ 统计服务 │      │
│  │User Svc  │ │Task Svc  │ │NotifySvc │ │Stats Svc │      │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │
└───────┼───────────┼───────────┼───────────┼───────────────┘
        │           │           │           │
        └───────────┴───────────┴───────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据层                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ PostgreSQL│ │  Redis   │ │ MongoDB  │ │ MinIO    │      │
│  │ (主数据库)│ │ (缓存)   │ │ (日志)   │ │ (文件)   │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 技术选型

### 2.1 后端技术栈
| 技术 | 选型 | 说明 |
|------|------|------|
| 语言 | Python 3.11+ | 生态丰富，开发效率高 |
| 框架 | FastAPI | 高性能，异步支持 |
| ORM | SQLAlchemy | 成熟稳定 |
| 数据库 | PostgreSQL 15 | 关系型，ACID支持 |
| 缓存 | Redis 7 | 高性能缓存 |
| 消息队列 | RabbitMQ / Kafka | 异步解耦 |

### 2.2 前端技术栈
| 技术 | 选型 | 说明 |
|------|------|------|
| 框架 | React 18 + TypeScript | 组件化开发 |
| UI库 | Ant Design / Material-UI | 企业级UI组件 |
| 状态管理 | Zustand | 轻量级状态管理 |
| 构建工具 | Vite | 快速构建 |

### 2.3 DevOps
| 技术 | 选型 | 说明 |
|------|------|------|
| 容器化 | Docker + K8s | 容器编排 |
| CI/CD | GitHub Actions | 自动化部署 |
| 监控 | Prometheus + Grafana | 可观测性 |
| 日志 | ELK Stack | 日志聚合 |

---

## 3. 服务拆分设计

### 3.1 用户服务 (User Service)
**职责**: 用户认证、授权、个人信息管理
**API接口**:
- POST /api/v1/auth/register - 用户注册
- POST /api/v1/auth/login - 用户登录
- GET /api/v1/users/:id - 获取用户信息
- PUT /api/v1/users/:id - 更新用户信息

**数据模型**:
```python
class User(Base):
    id: UUID (PK)
    username: String (unique)
    email: String (unique)
    password_hash: String
    avatar_url: String
    created_at: DateTime
    updated_at: DateTime
```

### 3.2 任务服务 (Task Service)
**职责**: 任务的增删改查、状态管理、分配
**API接口**:
- POST /api/v1/tasks - 创建任务
- GET /api/v1/tasks - 任务列表（支持筛选）
- GET /api/v1/tasks/:id - 任务详情
- PUT /api/v1/tasks/:id - 更新任务
- DELETE /api/v1/tasks/:id - 删除任务
- PATCH /api/v1/tasks/:id/status - 更新状态

**数据模型**:
```python
class Task(Base):
    id: UUID (PK)
    title: String
    description: Text
    status: Enum (TODO, IN_PROGRESS, DONE)
    priority: Enum (LOW, MEDIUM, HIGH, URGENT)
    assignee_id: UUID (FK → User)
    creator_id: UUID (FK → User)
    due_date: DateTime
    tags: Array[String]
    created_at: DateTime
    updated_at: DateTime

class Comment(Base):
    id: UUID (PK)
    task_id: UUID (FK → Task)
    user_id: UUID (FK → User)
    content: Text
    attachments: JSON
    created_at: DateTime
```

### 3.3 通知服务 (Notification Service)
**职责**: 消息推送、邮件通知、站内信
**通知类型**:
- 任务分配通知
- 截止日期提醒
- @提及通知
- 状态变更通知

---

## 4. 接口设计规范

### 4.1 RESTful API 设计原则
- 使用HTTP方法语义（GET/POST/PUT/PATCH/DELETE）
- URL使用名词复数形式
- 版本号放在URL中 (/api/v1/)
- 使用标准HTTP状态码

### 4.2 响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "timestamp": 1704067200
}
```

### 4.3 错误处理
```json
{
  "code": 40001,
  "message": "参数校验失败",
  "errors": [
    {
      "field": "title",
      "message": "任务标题不能为空"
    }
  ]
}
```

---

## 5. 安全设计

### 5.1 认证授权
- JWT Token认证
- OAuth2.0 第三方登录
- RBAC基于角色的权限控制

### 5.2 数据安全
- 敏感数据加密存储
- HTTPS传输加密
- SQL注入防护
- XSS攻击防护
- CSRF防护

---

## 6. 部署架构

### 6.1 开发环境
- Docker Compose本地编排
- 热重载开发模式
- Mock外部服务

### 6.2 生产环境
- Kubernetes集群部署
- 多副本负载均衡
- 自动扩缩容
- 灰度发布
- 数据库读写分离
"""
        
        logger.info("✅ 架构设计文档已生成")
        return architecture_doc


class WriteCode(Action):
    """
    动作：编写代码实现
    执行者：工程师
    """
    
    name = "WriteCode"
    
    async def run(self, architecture: str) -> str:
        """执行代码编写动作"""
        
        code_files = {
            "README.md": """# 智能任务管理系统

## 项目简介
高效、易用的团队任务管理系统，支持任务创建、分配、跟踪和协作。

## 技术栈
- **后端**: Python 3.11 + FastAPI + PostgreSQL + Redis
- **前端**: React 18 + TypeScript + Ant Design + Vite
- **基础设施**: Docker + Kubernetes + GitHub Actions

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 后端启动
\\`\\`\\`bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
\\`\\`\\`

### 前端启动
\\`\\`\\`bash
cd frontend
npm install
npm run dev
\\`\\`\\`

### Docker一键启动
\\`\\`\\`bash
docker-compose up -d
\\`\\`\\`

## 项目结构
\\`\\`\\`
backend/
├── app/
│   ├── api/          # API路由
│   ├── models/       # 数据模型
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # 业务逻辑
│   ├── core/         # 配置和工具
│   └── main.py       # 应用入口
├── tests/            # 测试用例
├── alembic/          # 数据库迁移
└── requirements.txt

frontend/
├── src/
│   ├── components/   # 公共组件
│   ├── pages/        # 页面组件
│   ├── hooks/        # 自定义hooks
│   ├── stores/       # 状态管理
│   ├── api/          # API调用
│   └── types/        # TypeScript类型
└── package.json
\\`\\`\\`

## 功能特性
- ✅ 任务CRUD操作
- ✅ 看板视图和列表视图
- ✅ 任务筛选和排序
- ✅ 团队协作和@提及
- ✅ 实时通知提醒
- ✅ 数据统计报表
- ✅ 权限管理

## License
MIT License
""",
            
            "backend/app/models/task.py": '''"""
任务数据模型定义
"""
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, Enum, DateTime, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.core.database import Base


class TaskStatus(PyEnum):
    """任务状态枚举"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(PyEnum):
    """任务优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False, comment="任务标题")
    description = Column(Text, nullable=True, comment="任务描述")
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False,
        comment="任务状态"
    )
    priority = Column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False,
        comment="任务优先级"
    )
    assignee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        comment="负责人ID"
    )
    creator_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        comment="创建者ID"
    )
    due_date = Column(DateTime, nullable=True, comment="截止日期")
    tags = Column(ARRAY(String), default=list, comment="标签列表")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )

    # 关系
    assignee = relationship("User", foreign_keys=[assignee_id])
    creator = relationship("User", foreign_keys=[creator_id])
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.title}>"
''',
            
            "backend/app/api/tasks.py": '''"""
任务API路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskQueryParams
)
from app.services.task_service import TaskService
from app.api.deps import get_current_user, get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(
    body: TaskCreate,
    current_user = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    创建新任务
    
    - **title**: 任务标题（必填）
    - **description**: 任务描述（可选）
    - **priority**: 优先级 low/medium/high/urgent
    - **assignee_id**: 负责人ID（可选）
    - **due_date**: 截止日期（可选）
    - **tags**: 标签列表（可选）
    """
    task = await task_service.create_task(body, creator_id=current_user.id)
    return task


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    status: Optional[str] = Query(None, description="按状态筛选"),
    priority: Optional[str] = Query(None, description="按优先级筛选"),
    assignee_id: Optional[UUID] = Query(None, description="按负责人筛选"),
    sort_by: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", description="排序方式 asc/desc"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    获取任务列表
    
    支持按状态、优先级、负责人筛选
    支持按不同字段排序
    支持分页
    """
    params = TaskQueryParams(
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        sort_by=sort_by,
        order=order,
        page=page,
        page_size=page_size
    )
    
    result = await task_service.get_tasks(params)
    return result


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    current_user = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """获取任务详情"""
    task = await task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    body: TaskUpdate,
    current_user = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """更新任务信息"""
    task = await task_service.update_task(task_id, body)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: UUID,
    status: str,
    current_user = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """更新任务状态"""
    valid_statuses = ["todo", "in_progress", "done"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"无效的状态值，可选: {valid_statuses}"
        )
    
    task = await task_service.update_task_status(task_id, status)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    current_user = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service)
):
    """删除任务"""
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
''',
            
            "frontend/src/components/TaskBoard.tsx": """/**
 * 任务看板组件
 * 支持拖拽排序和状态切换
 */

import React, { useState, useEffect } from 'react';
import { Card, Tag, Avatar, Space, Dropdown, Modal, Input, Button } from 'antd';
import {
  MoreOutlined,
  CalendarOutlined,
  UserOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import type { Task, TaskStatus } from '../types/task';
import { taskApi } from '../api/task';

interface TaskBoardProps {
  projectId?: string;
}

const COLUMNS = [
  { id: 'todo', title: '待办', color: '#999' },
  { id: 'in_progress', title: '进行中', color: '#1890ff' },
  { id: 'done', title: '已完成', color: '#52c41a' },
];

const PRIORITY_COLORS: Record<string, string> = {
  low: 'green',
  medium: 'orange',
  high: 'red',
  urgent: 'volcano',
};

export const TaskBoard: React.FC<TaskBoardProps> = ({ projectId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTasks();
  }, [projectId]);

  const fetchTasks = async () => {
    setLoading(true);
    try {
      const data = await taskApi.getTasks({ project_id: projectId });
      setTasks(data.items);
    } finally {
      setLoading(false);
    }
  };

  const handleDragEnd = async (result: any) => {
    if (!result.destination) return;

    const taskId = result.draggableId;
    const newStatus = result.destination.droppableId as TaskStatus;

    await taskApi.updateTaskStatus(taskId, newStatus);
    fetchTasks();
  };

  const getTasksByStatus = (status: TaskStatus) => {
    return tasks.filter(task => task.status === status);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div style={{ display: 'flex', gap: 16, overflowX: 'auto', padding: '16px 0' }}>
        {COLUMNS.map(column => (
          <div
            key={column.id}
            style={{
              flex: 1,
              minWidth: 300,
              backgroundColor: '#f5f5f5',
              borderRadius: 8,
              padding: 16,
            }}
          >
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: 16,
            }}>
              <span style={{ fontWeight: 600, color: column.color }}>
                {column.title}
              </span>
              <Tag>{getTasksByStatus(column.id as TaskStatus).length}</Tag>
            </div>

            <Droppable droppableId={column.id}>
              {(provided, snapshot) => (
                <div
                  ref={provided.innerRef}
                  {...provided.droppableProps}
                  style={{
                    minHeight: 200,
                    backgroundColor: snapshot.isDraggingOver ? '#e6f7ff' : 'transparent',
                    borderRadius: 4,
                    padding: 4,
                  }}
                >
                  {getTasksByStatus(column.id as TaskStatus).map((task, index) => (
                    <Draggable key={task.id} draggableId={task.id} index={index}>
                      {(provided, snapshot) => (
                        <Card
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          size="small"
                          style={{
                            marginBottom: 8,
                            boxShadow: snapshot.isDragging ? '0 4px 12px rgba(0,0,0,0.15)' : 'none',
                            ...provided.draggableProps.style,
                          }}
                          actions={[
                            <MoreOutlined key="more" />,
                          ]}
                        >
                          <p style={{ fontWeight: 500, marginBottom: 8 }}>
                            {task.title}
                          </p>
                          
                          {task.description && (
                            <p style={{ color: '#666', fontSize: 12, marginBottom: 8 }}>
                              {task.description.slice(0, 80)}...
                            </p>
                          )}

                          <Space size="small" wrap>
                            <Tag color={PRIORITY_COLORS[task.priority]}>
                              {{ low: '低', medium: '中', high: '高', urgent: '紧急' }[task.priority]}
                            </Tag>
                            
                            {task.due_date && (
                              <Tag icon={<CalendarOutlined />}>
                                {new Date(task.due_date).toLocaleDateString()}
                              </Tag>
                            )}
                            
                            {task.assignee && (
                              <Avatar size="small" icon={<UserOutlined />} />
                            )}
                          </Space>
                        </Card>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>

            <Button
              type="dashed"
              icon={<PlusOutlined />}
              block
              style={{ marginTop: 8 }}
              onClick={() => {/* 打开创建任务弹窗 */}}
            >
              添加任务
            </Button>
          </div>
        ))}
      </div>
    </DragDropContext>
  );
};
'''
        }
        
        logger.info(f"✅ 代码文件已生成，共 {len(code_files)} 个文件")
        return str(list(code_files.keys()))


class WriteTestCases(Action):
    """
    动作：编写测试用例
    执行者：测试工程师
    """
    
    name = "WriteTestCases"
    
    async def run(self, code_info: str) -> str:
        """执行测试用例编写动作"""
        
        test_cases = '''
# 测试计划与用例

## 1. 测试策略

### 1.1 测试层次
```
┌─────────────────────────────────────┐
│         E2E测试 (Playwright)        │  ← 用户场景验证
├─────────────────────────────────────┤
│         集成测试 (pytest)            │  ← API集成测试
├─────────────────────────────────────┤
│         单元测试 (pytest)            │  ← 函数/方法级别
└─────────────────────────────────────┘
```

### 1.2 测试覆盖率目标
- 单元测试覆盖率: ≥ 80%
- 核心业务逻辑覆盖率: ≥ 90%
- API接口测试覆盖率: 100%

---

## 2. 单元测试用例

### 2.1 任务服务单元测试

```python
# tests/unit/test_task_service.py
"""任务服务单元测试"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task, TaskStatus, TaskPriority


@pytest.fixture
def task_service():
    """创建任务服务实例"""
    mock_repo = Mock()
    mock_notification = Mock()
    return TaskService(mock_repo, mock_notification)


@pytest.fixture
def sample_task_data():
    """示例任务数据"""
    return TaskCreate(
        title="测试任务",
        description="这是一个测试任务",
        priority=TaskPriority.HIGH,
        due_date=datetime.utcnow() + timedelta(days=7),
        tags=["test", "unit-test"]
    )


class TestTaskCreation:
    """任务创建测试套件"""
    
    @pytest.mark.asyncio
    async def test_create_task_success(self, task_service, sample_task_data):
        """测试正常创建任务"""
        # Arrange
        creator_id = "user-123"
        task_service.repo.create = AsyncMock(return_value=Task(
            id="task-456",
            **sample_task_data.model_dump(),
            creator_id=creator_id,
            status=TaskStatus.TODO
        ))
        
        # Act
        result = await task_service.create_task(sample_task_data, creator_id)
        
        # Assert
        assert result is not None
        assert result.title == "测试任务"
        assert result.status == TaskStatus.TODO
        assert result.creator_id == creator_id
        task_service.repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_task_with_empty_title(self, task_service):
        """测试创建任务时标题为空"""
        with pytest.raises(ValueError, match="任务标题不能为空"):
            invalid_data = TaskCreate(title="", priority=TaskPriority.MEDIUM)
            await task_service.create_task(invalid_data, "user-123")

    @pytest.mark.asyncio
    async def test_create_task_with_past_due_date(self, task_service):
        """测试创建任务时截止日期是过去的时间"""
        past_date = datetime.utcnow() - timedelta(days=1)
        invalid_data = TaskCreate(
            title="过期任务",
            due_date=past_date
        )
        
        with pytest.raises(ValueError, match="截止日期不能是过去的时间"):
            await task_service.create_task(invalid_data, "user-123")


class TestTaskStatusUpdate:
    """任务状态更新测试套件"""
    
    @pytest.mark.asyncio
    async def test_update_status_todo_to_in_progress(self, task_service):
        """测试状态从待办变为进行中"""
        task = Task(id="task-1", title="测试", status=TaskStatus.TODO)
        task_service.repo.get_by_id = AsyncMock(return_value=task)
        task_service.repo.update = AsyncMock(return_value=task)
        
        result = await task_service.update_task_status("task-1", "in_progress")
        
        assert result.status == TaskStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_update_status_invalid_transition(self, task_service):
        """测试无效的状态转换"""
        task = Task(id="task-1", title="测试", status=TaskStatus.DONE)
        task_service.repo.get_by_id = AsyncMock(return_value=task)
        
        # 已完成的任务不能回到待办（业务规则限制）
        with pytest.raises(ValueError, match="无效的状态转换"):
            await task_service.update_task_status("task-1", "todo")


class TestTaskFiltering:
    """任务筛选测试套件"""
    
    @pytest.mark.asyncio
    async def test_filter_by_status(self, task_service):
        """测试按状态筛选"""
        task_service.repo.filter = AsyncMock(return_value=[
            Task(id="t1", title="任务1", status=TaskStatus.IN_PROGRESS),
            Task(id="t2", title="任务2", status=TaskStatus.IN_PROGRESS),
        ])
        
        params = {"status": "in_progress"}
        result = await task_service.get_tasks(params)
        
        assert len(result.items) == 2
        for task in result.items:
            assert task.status == TaskStatus.IN_PROGRESS

    @pytest.mark.asyncio
    async def test_filter_by_priority_and_assignee(self, task_service):
        """测试按优先级和负责人组合筛选"""
        task_service.repo.filter = AsyncMock(return_value=[
            Task(id="t1", title="高优任务", priority=TaskPriority.HIGH),
        ])
        
        params = {
            "priority": "high",
            "assignee_id": "user-123"
        }
        result = await task_service.get_tasks(params)
        
        assert len(result.items) == 1
        assert result.items[0].priority == TaskPriority.HIGH
```

### 2.2 API集成测试

```python
# tests/integration/test_task_api.py
"""任务API集成测试"""
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """创建测试客户端"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers():
    """认证头"""
    # 使用测试token
    return {"Authorization": "Bearer test-token"}


class TestTaskAPI:
    """任务API测试套件"""
    
    @pytest.mark.asyncio
    async def test_create_task_api(self, client, auth_headers):
        """测试创建任务API"""
        payload = {
            "title": "API测试任务",
            "description": "通过API创建的任务",
            "priority": "medium",
            "due_date": "2024-12-31T23:59:59Z",
            "tags": ["api-test"]
        }
        
        response = await client.post(
            "/api/v1/tasks",
            json=payload,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["title"] == "API测试任务"
        assert "id" in data["data"]

    @pytest.mark.asyncio
    async def test_get_task_list_api(self, client, auth_headers):
        """测试获取任务列表API"""
        response = await client.get(
            "/api/v1/tasks?status=in_progress&page=1&page_size=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data["data"]
        assert "total" in data["data"]
        assert "page" in data["data"]

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, client, auth_headers):
        """测试获取不存在的任务"""
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        
        response = await client.get(
            f"/api/v1/tasks/{non_existent_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task_status_api(self, client, auth_headers):
        """测试更新任务状态API"""
        task_id = "existing-task-id"
        
        response = await client.patch(
            f"/api/v1/tasks/{task_id}/status?status=done",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "done"

    @pytest.mark.asyncio
    async def test_invalid_status_value(self, client, auth_headers):
        """测试无效的状态值"""
        task_id = "existing-task-id"
        
        response = await client.patch(
            f"/api/v1/tasks/{task_id}/status?status=invalid_status",
            headers=auth_headers
        )
        
        assert response.status_code == 400
```

---

## 3. E2E测试用例

### 3.1 核心用户流程测试

```typescript
// tests/e2e/task-management.spec.ts
/** 
 * 任务管理 E2E 测试
 * 使用 Playwright 进行端到端测试
 */
import { test, expect } from '@playwright/test';

test.describe('任务管理核心流程', () => {
  
  test.beforeEach(async ({ page }) => {
    // 登录
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/dashboard');
  });

  test('完整任务生命周期', async ({ page }) => {
    // 1. 创建任务
    await page.click('[data-testid="create-task-button"]');
    await page.fill('[data-testid="task-title"]', 'E2E测试任务');
    await page.fill('[data-testid="task-description"]', '这是端到端测试');
    await page.selectOption('[data-testid="task-priority"]', 'high');
    await page.click('[data-testid="submit-task"]');
    
    // 验证任务创建成功
    await expect(page.locator('[data-testid="task-item"]')).toContainText('E2E测试任务');
    
    // 2. 查看任务详情
    await page.click('[data-testid="task-item"]:has-text("E2E测试任务")');
    await expect(page.locator('[data-testid="task-detail-title"]')).toHaveText('E2E测试任务');
    
    // 3. 更新任务状态（拖拽到进行中）
    await page.goBack();
    const taskItem = page.locator('[data-testid="task-item"]:has-text("E2E测试任务")');
    const todoColumn = page.locator('[data-testid="column-todo"]');
    const inProgressColumn = page.locator('[data-testid="column-in-progress"]');
    
    await taskItem.dragTo(inProgressColumn);
    
    // 验证状态已更新
    await expect(inProgressColumn.locator('[data-testid="task-item"]')).toHaveCount(1);
    
    // 4. 添加评论
    await page.click('[data-testid="task-item"]:has-text("E2E测试任务")');
    await page.fill('[data-testid="comment-input"]', '任务正在进行中');
    await page.click('[data-testid="submit-comment"]');
    
    // 验证评论已添加
    await expect(page.locator('[data-testid="comment-item"]')).toContainText('任务正在进行中');
    
    // 5. 完成任务
    await page.goBack();
    const doneColumn = page.locator('[data-testid="column-done"]');
    await taskItem.dragTo(doneColumn);
    
    // 验证任务已完成
    await expect(doneColumn.locator('[data-testid="task-item"]')).toHaveText('E2E测试任务');
  });

  test('任务筛选功能', async ({ page }) => {
    // 创建不同状态的任务
    // ... 创建任务的代码
    
    // 按状态筛选
    await page.selectOption('[data-testid="filter-status"]', 'in_progress');
    await expect(page.locator('[data-testid="task-item"]')).toHaveCount(2); // 假设有2个进行中的任务
    
    // 按优先级筛选
    await page.selectOption('[data-testid="filter-priority"]', 'high');
    await expect(page.locator('[data-testid="task-item"]')).toHaveCount(1); // 假设有1个高优先级任务
    
    // 重置筛选
    await page.click('[data-testid="reset-filter"]');
    await expect(page.locator('[data-testid="task-item"]')).toHaveCountGreaterThan(0);
  });
});
```

---

## 4. 性能测试

### 4.1 API性能基准测试

```python
# tests/performance/test_api_performance.py
"""API性能测试"""
import locust
from locust import HttpUser, task, between

class TaskAPIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # 登录获取token
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password"
        })
        self.token = response.json()["data"]["access_token"]

    @task(5)
    def get_task_list(self):
        """获取任务列表（高频操作）"""
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/v1/tasks?page=1&page_size=20", headers=headers)

    @task(3)
    def get_task_detail(self):
        """获取任务详情"""
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/v1/tasks/some-task-id", headers=headers)

    @task(2)
    def create_task(self):
        """创建任务"""
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post("/api/v1/tasks", json={
            "title": "Load Test Task",
            "priority": "medium"
        }, headers=headers)

    @task(1)
    def update_task_status(self):
        """更新任务状态"""
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.patch("/api/v1/tasks/some-task-id/status?status=done", headers=headers)
```

### 4.2 性能指标
| 指标 | 目标值 | 备注 |
|------|--------|------|
| API响应时间(P50) | < 200ms | 一般请求 |
| API响应时间(P99) | < 500ms | 含复杂查询 |
| 并发用户数 | 100+ | 正常负载 |
| 峰值QPS | 500+ | 大促场景 |
| 错误率 | < 0.1% | 5xx错误 |

---

## 5. 测试执行命令

```bash
# 运行单元测试
pytest tests/unit/ -v --cov=app --cov-report=html

# 运行集成测试
pytest tests/integration/ -v

# 运行E2E测试
npx playwright test tests/e2e/

# 运行性能测试
locust -f tests/performance/test_api_performance.py

# 运行全部测试
pytest tests/ -v --cov=app
```

---
**测试文档版本**: v1.0
**创建日期**: 2024年
**维护者**: QA团队
'''
        
        logger.info("✅ 测试用例文档已生成")
        return test_cases


# ============================================================
# 2. 自定义 Role（角色）
# ============================================================

class ProductManager(Role):
    """
    产品经理角色
    职责：需求分析、PRD撰写、产品规划
    """
    
    name = "Alice"
    profile = "Product Manager"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.actions = [WritePRD]
        self._watch = {WritePRD}
        
    async def _think(self):
        """决定下一步动作"""
        if self._rc.news:  # 如果有新的消息（需求）
            self._set_action(WritePRD, run_async=True)


class Architect(Role):
    """
    架构师角色
    职责：系统设计、技术选型、架构文档
    """
    
    name = "Bob"
    profile = "Architect"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.actions = [DesignArchitecture]
        self._watch = {DesignArchitecture}
    
    async def _think(self):
        """决定下一步动作"""
        if self._rc.news:  # 如果收到PRD
            self._set_action(DesignArchitecture, run_async=True)


class Engineer(Role):
    """
    工程师角色
    职责：代码实现、单元测试
    """
    
    name = "Charlie"
    profile = "Senior Engineer"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.actions = [WriteCode]
        self._watch = {WriteCode}
    
    async def _think(self):
        """决定下一步动作"""
        if self._rc.news:  # 如果收到架构设计
            self._set_action(WriteCode, run_async=True)


class QaEngineer(Role):
    """
    测试工程师角色
    职责：测试计划、测试用例、质量保障
    """
    
    name = "Diana"
    profile = "QA Engineer"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.actions = [WriteTestCases]
        self._watch = {WriteTestCases}
    
    async def _think(self):
        """决定下一步动作"""
        if self._rc.news:  # 如果收到代码
            self._set_action(WriteTestCases, run_async=True)


# ============================================================
# 3. 组装团队并运行
# ============================================================

async def main():
    """运行 MetaGPT 软件公司模拟"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       🏢 MetaGPT 入门教程 - 模拟软件公司运作                  ║
║                                                              ║
║  核心概念学习要点:                                            ║
║  ─────────────────                                           ║
║  1. Role: 公司职位，每个Role有专门的职责和能力               ║
║  2. Action: 角色执行的具体动作（如写PRD、写代码）            ║
║  3. Environment: 公司环境，角色在其中协作和通信               ║
║  4. Message: 角色间传递的消息载体                            ║
║  5. SOP: 标准作业流程，定义工作顺序                          ║
║  6. Team: 团队组织，协调多个角色协同工作                    ║
║                                                              ║
║  本示例模拟的软件开发流程:                                    ║
║  ─────────────────                                           ║
║  📋 产品经理(Alice) → PRD文档                                ║
║       ↓                                                      ║
║  🏗️ 架构师(Bob) → 架构设计文档                               ║
║       ↓                                                      ║
║  👨‍💻 工程师(Charlie) → 代码实现                             ║
║       ↓                                                      ║
║  🧪 测试工程师(Diana) → 测试用例                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    print("\n" + "="*70)
    print("  🚀 启动虚拟软件公司...")
    print("="*70 + "\n")
    
    # 定义公司需求
    company_requirement = """
    我们需要开发一个智能任务管理系统，用于帮助团队更好地管理工作任务。
    系统需要支持任务的创建、分配、跟踪和协作，提高团队工作效率。
    目标用户是中小型技术团队的成员。
    """
    
    print("📋 公司需求:")
    print("-" * 70)
    print(company_requirement.strip())
    print("-" * 70 + "\n")
    
    print("👥 团队成员:")
    print("  1. Alice - 产品经理 (Product Manager)")
    print("  2. Bob   - 架构师 (Architect)")
    print("  3. Charlie - 高级工程师 (Senior Engineer)")
    print("  4. Diana - 测试工程师 (QA Engineer)")
    print()
    
    # 创建公司环境
    env = Environment(desc="软件开发团队环境")
    
    # 招聘员工（创建角色实例）
    pm = ProductManager()
    architect = Architect()
    engineer = Engineer()
    qa = QaEngineer()
    
    # 组建团队
    team = Team(
        roles=[pm, architect, engineer, qa],
        env=env,
        desc="智能任务管理系统开发团队",
    )
    
    print("🔄 开始工作流程...\n")
    print("="*70)
    
    # 投入需求，启动工作流
    try:
        result = await team.run(company_requirement)
        
        print("\n" + "="*70)
        print("  ✅ 项目开发完成！")
        print("="*70)
        print("\n📦 交付物清单:")
        print("  ✓ 产品需求文档 (PRD)")
        print("  ✓ 系统架构设计文档")
        print("  ✓ 源代码实现（后端+前端）")
        print("  ✓ 测试计划和测试用例")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("\n💡 提示：")
        print("   1. 请确保已安装 metagpt: pip install metagpt")
        print("   2. 请设置 OPENAI_API_KEY 环境变量")


if __name__ == "__main__":
    asyncio.run(main())
