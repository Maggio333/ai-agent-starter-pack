# tests/test_property_based_metadata.py
import sys
sys.path.append('.')
from domain import (
    RAGChunk, ChatMessage, RAGChunkMetadata, 
    MetadataField, MetadataFieldRegistry, MetadataFieldMapper
)

def test_property_based_metadata():
    """Test the new property-based metadata system"""
    print("🧪 Testing Property-Based Metadata System...")
    
    # Test field registry
    print("📋 Testing MetadataFieldRegistry...")
    
    # Test field definitions
    text_length_field = MetadataField.TEXT_LENGTH
    definition = MetadataFieldRegistry.get_field_definition(text_length_field)
    assert definition["type"] == int
    assert definition["default"] == 0
    assert definition["description"] == "Length of text content"
    
    print("✅ Field definition test passed!")
    
    # Test field type
    field_type = MetadataFieldRegistry.get_field_type(MetadataField.WORD_COUNT)
    assert field_type == int
    
    print("✅ Field type test passed!")
    
    # Test field default
    default_value = MetadataFieldRegistry.get_field_default(MetadataField.SCORE)
    assert default_value is None
    
    print("✅ Field default test passed!")
    
    # Test field mapper
    print("🔄 Testing MetadataFieldMapper...")
    
    # Test field to key conversion
    key = MetadataFieldMapper.field_to_key(MetadataField.ENTITY_TYPE)
    assert key == "entity_type"
    
    print("✅ Field to key conversion test passed!")
    
    # Test key to field conversion
    field = MetadataFieldMapper.key_to_field("entity_id")
    assert field == MetadataField.ENTITY_ID
    
    print("✅ Key to field conversion test passed!")
    
    # Test required fields
    required_fields = MetadataFieldMapper.get_required_fields()
    assert MetadataField.ENTITY_TYPE in required_fields
    assert MetadataField.ENTITY_ID in required_fields
    
    print("✅ Required fields test passed!")
    
    # Test field validation
    is_valid = MetadataFieldMapper.validate_field_value(MetadataField.TEXT_LENGTH, 100)
    assert is_valid is True
    
    is_invalid = MetadataFieldMapper.validate_field_value(MetadataField.TEXT_LENGTH, "invalid")
    assert is_invalid is False
    
    print("✅ Field validation test passed!")
    
    # Test field schema
    schema = MetadataFieldMapper.get_field_schema()
    assert "entity_type" in schema
    assert "text_length" in schema
    assert schema["entity_type"]["type"] == "str"
    assert schema["text_length"]["type"] == "int"
    
    print("✅ Field schema test passed!")
    
    return True

def test_rag_chunk_property_based_metadata():
    """Test RAGChunk with property-based metadata"""
    print("🧪 Testing RAGChunk Property-Based Metadata...")
    
    # Create RAG chunk
    chunk = RAGChunk.create_high_quality("Test text with @mention and #hashtag")
    metadata = chunk.get_metadata()
    
    # Test that metadata uses property-based system
    metadata_dict = metadata.to_dict()
    
    # Check that keys come from field registry
    assert MetadataFieldMapper.field_to_key(MetadataField.TEXT_LENGTH) in metadata_dict
    assert MetadataFieldMapper.field_to_key(MetadataField.WORD_COUNT) in metadata_dict
    assert MetadataFieldMapper.field_to_key(MetadataField.SCORE) in metadata_dict
    assert MetadataFieldMapper.field_to_key(MetadataField.QUALITY_LEVEL) in metadata_dict
    
    print("✅ Property-based keys test passed!")
    
    # Test that values are correct
    assert metadata_dict[MetadataFieldMapper.field_to_key(MetadataField.TEXT_LENGTH)] > 0
    assert metadata_dict[MetadataFieldMapper.field_to_key(MetadataField.WORD_COUNT)] > 0
    assert metadata_dict[MetadataFieldMapper.field_to_key(MetadataField.SCORE)] == 0.9
    assert metadata_dict[MetadataFieldMapper.field_to_key(MetadataField.QUALITY_LEVEL)] == "high"
    
    print("✅ Property-based values test passed!")
    
    # Test deserialization
    restored_metadata = RAGChunkMetadata.from_dict(metadata_dict)
    assert isinstance(restored_metadata, RAGChunkMetadata)
    assert restored_metadata.text_length == metadata.text_length
    assert restored_metadata.word_count == metadata.word_count
    assert restored_metadata.score == metadata.score
    
    print("✅ Property-based deserialization test passed!")
    
    return True

def test_no_more_hardcoded_strings():
    """Test that there are no more hardcoded strings"""
    print("🧪 Testing No More Hardcoded Strings...")
    
    # Test that all field keys come from enum
    all_fields = MetadataFieldRegistry.get_all_fields()
    
    for field in all_fields:
        key = MetadataFieldMapper.field_to_key(field)
        # Verify that key is not hardcoded but comes from enum
        assert key == field.value
        assert isinstance(key, str)
        assert len(key) > 0
    
    print("✅ No hardcoded strings test passed!")
    
    # Test that we can get all field information dynamically
    schema = MetadataFieldMapper.get_field_schema()
    
    for field in all_fields:
        field_key = MetadataFieldMapper.field_to_key(field)
        assert field_key in schema
        
        field_info = schema[field_key]
        assert "type" in field_info
        assert "required" in field_info
        assert "description" in field_info
    
    print("✅ Dynamic field information test passed!")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Property-Based Metadata tests...\n")
    
    try:
        test_property_based_metadata()
        test_rag_chunk_property_based_metadata()
        test_no_more_hardcoded_strings()
        
        print("\n🎉 ALL PROPERTY-BASED METADATA TESTS PASSED! 🎉")
        print("✅ Field registry system")
        print("✅ Field mapper system")
        print("✅ Property-based serialization")
        print("✅ No more hardcoded strings!")
        print("✅ Type safety and validation")
        print("✅ Dynamic field definitions")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
