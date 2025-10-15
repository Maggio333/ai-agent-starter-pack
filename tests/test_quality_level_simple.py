# tests/test_quality_level_simple.py
import sys
sys.path.append('.')
from domain import QualityLevel, RAGChunk

def test_quality_level():
    """Simple test for QualityLevel enum"""
    print("🧪 Testing QualityLevel enum...")
    
    # Test values
    assert QualityLevel.HIGH.value == "high"
    assert QualityLevel.MEDIUM.value == "medium"
    assert QualityLevel.LOW.value == "low"
    assert QualityLevel.UNKNOWN.value == "unknown"
    
    print("✅ QualityLevel values test passed!")
    
    # Test from_score
    assert QualityLevel.from_score(0.9) == QualityLevel.HIGH
    assert QualityLevel.from_score(0.7) == QualityLevel.MEDIUM
    assert QualityLevel.from_score(0.3) == QualityLevel.LOW
    assert QualityLevel.from_score(None) == QualityLevel.UNKNOWN
    
    print("✅ QualityLevel from_score test passed!")
    
    # Test properties
    assert QualityLevel.HIGH.is_high_quality is True
    assert QualityLevel.MEDIUM.is_medium_quality is True
    assert QualityLevel.LOW.is_low_quality is True
    assert QualityLevel.UNKNOWN.is_unknown_quality is True
    
    print("✅ QualityLevel properties test passed!")
    
    # Test thresholds
    assert QualityLevel.HIGH.threshold == 0.8
    assert QualityLevel.MEDIUM.threshold == 0.5
    assert QualityLevel.LOW.threshold == 0.0
    
    print("✅ QualityLevel thresholds test passed!")
    
    return True

def test_rag_chunk_with_quality_level():
    """Test RAGChunk with QualityLevel enum"""
    print("🧪 Testing RAGChunk with QualityLevel...")
    
    # Test high quality chunk
    chunk = RAGChunk.create_high_quality("Test text")
    assert chunk.get_quality_level() == QualityLevel.HIGH
    assert chunk.is_high_quality() is True
    assert chunk.is_medium_quality() is False
    assert chunk.is_low_quality() is False
    
    print("✅ High quality chunk test passed!")
    
    # Test medium quality chunk
    chunk = RAGChunk.create_medium_quality("Test text")
    assert chunk.get_quality_level() == QualityLevel.MEDIUM
    assert chunk.is_high_quality() is False
    assert chunk.is_medium_quality() is True
    assert chunk.is_low_quality() is False
    
    print("✅ Medium quality chunk test passed!")
    
    # Test low quality chunk
    chunk = RAGChunk.create_from_text("Test text", score=0.3)
    assert chunk.get_quality_level() == QualityLevel.LOW
    assert chunk.is_high_quality() is False
    assert chunk.is_medium_quality() is False
    assert chunk.is_low_quality() is True
    
    print("✅ Low quality chunk test passed!")
    
    # Test unknown quality chunk
    chunk = RAGChunk.create_from_text("Test text", score=None)
    assert chunk.get_quality_level() == QualityLevel.UNKNOWN
    assert chunk.is_high_quality() is False
    assert chunk.is_medium_quality() is False
    assert chunk.is_low_quality() is False
    
    print("✅ Unknown quality chunk test passed!")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting QualityLevel tests...\n")
    
    try:
        test_quality_level()
        test_rag_chunk_with_quality_level()
        
        print("\n🎉 ALL QUALITY LEVEL TESTS PASSED! 🎉")
        print("✅ QualityLevel enum")
        print("✅ RAGChunk integration")
        print("✅ No more magic strings!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
