import pytest
from datetime import datetime, timedelta

from application.services.prompt_service import PromptService
from domain.entities.chat_message import ChatMessage, MessageRole


def make_msg(role: MessageRole, content: str, ts: datetime) -> ChatMessage:
    return ChatMessage(role=role, content=content, timestamp=ts)


class TestPromptService:
    def setup_method(self):
        self.service = PromptService()

    def test_system_prompts_are_combined_into_single_message(self):
        now = datetime.now()
        history: list[ChatMessage] = []

        messages = self.service.build_complete_message_list(
            user_message="Hello",
            idioms=["Rule A", "Rule B"],
            conversation_history=history,
            user_context=None,
        )

        system_msgs = [m for m in messages if m.role == MessageRole.SYSTEM]
        assert len(system_msgs) == 1, "All system prompts should be combined into a single SYSTEM message"
        assert "### PERSONA" in system_msgs[0].content
        assert "### FORMAT" in system_msgs[0].content
        assert "### ROLE" in system_msgs[0].content
        assert "### IDIOMS" in system_msgs[0].content

    def test_alternation_user_assistant_history_then_user(self):
        base = datetime.now()
        # History with proper alternation ending with assistant
        history = [
            make_msg(MessageRole.USER, "u1", base + timedelta(seconds=1)),
            make_msg(MessageRole.ASSISTANT, "a1", base + timedelta(seconds=2)),
            make_msg(MessageRole.USER, "u2", base + timedelta(seconds=3)),
            make_msg(MessageRole.ASSISTANT, "a2", base + timedelta(seconds=4)),
        ]

        messages = self.service.build_complete_message_list(
            user_message="current user",
            idioms=[],
            conversation_history=history,
            user_context=None,
        )

        # After single SYSTEM, we expect history (u,a,...) then the new USER
        non_system = [m for m in messages if m.role != MessageRole.SYSTEM]
        assert non_system[0].role == MessageRole.USER, "First non-system message must be USER"
        assert non_system[-1].role == MessageRole.USER, "Last message must be the current USER message"

        # Check alternation within history part (skip the last current USER)
        history_only = non_system[:-1]
        for i in range(len(history_only) - 1):
            assert history_only[i].role != history_only[i + 1].role, "History messages must alternate USER/ASSISTANT"

    def test_if_history_ends_with_user_it_is_trimmed_before_adding_new_user(self):
        base = datetime.now()
        # History ends with USER (should be trimmed)
        history = [
            make_msg(MessageRole.USER, "u1", base + timedelta(seconds=1)),
            make_msg(MessageRole.ASSISTANT, "a1", base + timedelta(seconds=2)),
            make_msg(MessageRole.USER, "u2", base + timedelta(seconds=3)),
        ]

        messages = self.service.build_complete_message_list(
            user_message="current user",
            idioms=[],
            conversation_history=history,
            user_context=None,
        )

        non_system = [m for m in messages if m.role != MessageRole.SYSTEM]
        # Ensure there are not two USERs at the end
        assert not (non_system[-2].role == MessageRole.USER and non_system[-1].role == MessageRole.USER), (
            "Should not produce USER followed by USER at the end"
        )


