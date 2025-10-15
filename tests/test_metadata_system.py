# tests/test_metadata_system.py
import sys
sys.path.append('.')
from domain import RAGChunk, ChatMessage, RAGChunkMetadata, ChatMessageMetadata, MetadataFactory, MetadataType, BaseMetadata

def test_metadata_system():
    """Test the new structured metadata system"""
    print("🧪 Testing Metadata System...")
    
    # Test RAGChunk metadata
    chunk = RAGChunk.create_high_quality("Test text with @mention and #hashtag")
    metadata = chunk.get_metadata()
    
    assert isinstance(metadata, RAGChunkMetadata)
    assert metadata.entity_type == MetadataType.RAG_CHUNK
    assert metadata.entity_id == chunk.chunk_id
    assert metadata.text_length > 0
    assert metadata.word_count > 0
    assert metadata.score == 0.9
    assert metadata.quality_level == "high"
    assert metadata.has_text_content is True
    assert metadata.mentions_count == 1
    assert metadata.hashtags_count == 1
    
    print("✅ RAGChunk metadata test passed!")
    
    # Test ChatMessage metadata
    message = ChatMessage.create_user_message("Hello world! This is a test message.")
    message_metadata = message.get_metadata()
    
    assert isinstance(message_metadata, ChatMessageMetadata)
    assert message_metadata.entity_type == MetadataType.CHAT_MESSAGE
    assert message_metadata.entity_id == message.message_id
    assert message_metadata.word_count > 0
    assert message_metadata.character_count > 0
    assert message_metadata.is_long_message is False
    
    print("✅ ChatMessage metadata test passed!")
    
    # Test metadata serialization
    metadata_dict = metadata.to_dict()
    assert isinstance(metadata_dict, dict)
    assert "entity_type" in metadata_dict
    assert "entity_id" in metadata_dict
    assert "text_length" in metadata_dict
    assert "quality_level" in metadata_dict
    
    print("✅ Metadata serialization test passed!")
    
    # Test metadata deserialization
    restored_metadata = RAGChunkMetadata.from_dict(metadata_dict)
    assert isinstance(restored_metadata, RAGChunkMetadata)
    assert restored_metadata.entity_type == metadata.entity_type
    assert restored_metadata.entity_id == metadata.entity_id
    assert restored_metadata.text_length == metadata.text_length
    
    print("✅ Metadata deserialization test passed!")
    
    # Test custom fields
    metadata.add_custom_field("custom_field", "custom_value")
    assert metadata.has_custom_field("custom_field") is True
    assert metadata.get_custom_field("custom_field") == "custom_value"
    
    metadata.remove_custom_field("custom_field")
    assert metadata.has_custom_field("custom_field") is False
    
    print("✅ Custom fields test passed!")
    
    return True

def test_metadata_factory():
    """Test MetadataFactory"""
    print("🧪 Testing MetadataFactory...")
    
    # Test RAG chunk metadata creation
    rag_metadata = MetadataFactory.create_rag_chunk_metadata(
        chunk_id="test_chunk",
        text_length=100,
        word_count=20,
        score=0.8,
        quality_level="high"
    )
    
    assert isinstance(rag_metadata, RAGChunkMetadata)
    assert rag_metadata.entity_id == "test_chunk"
    assert rag_metadata.text_length == 100
    assert rag_metadata.word_count == 20
    assert rag_metadata.score == 0.8
    assert rag_metadata.quality_level == "high"
    
    print("✅ RAG chunk metadata factory test passed!")
    
    # Test chat message metadata creation
    message_metadata = MetadataFactory.create_chat_message_metadata(
        message_id="test_message",
        word_count=15,
        character_count=75,
        is_question=True
    )
    
    assert isinstance(message_metadata, ChatMessageMetadata)
    assert message_metadata.entity_id == "test_message"
    assert message_metadata.word_count == 15
    assert message_metadata.character_count == 75
    assert message_metadata.is_question is True
    
    print("✅ Chat message metadata factory test passed!")
    
    # Test base metadata creation
    base_metadata = MetadataFactory.create_base_metadata(
        entity_type=MetadataType.CONVERSATION,
        entity_id="test_conversation"
    )
    
    assert isinstance(base_metadata, BaseMetadata)
    assert base_metadata.entity_type == MetadataType.CONVERSATION
    assert base_metadata.entity_id == "test_conversation"
    
    print("✅ Base metadata factory test passed!")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Metadata System tests...\n")
    
    try:
        test_metadata_system()
        test_metadata_factory()
        
        print("\n🎉 ALL METADATA SYSTEM TESTS PASSED! 🎉")
        print("✅ Structured metadata models")
        print("✅ No more hardcoded dictionaries!")
        print("✅ Type safety and validation")
        print("✅ Serialization/deserialization")
        print("✅ Custom fields support")
        print("✅ Factory pattern")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
