# domain/entities/quality_level.py
from enum import Enum

class QualityLevel(Enum):
    """Quality level enumeration for RAG chunks"""
    UNKNOWN = "unknown"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
    @classmethod
    def from_score(cls, score: float) -> 'QualityLevel':
        """Create QualityLevel from score"""
        if score is None:
            return cls.UNKNOWN
        elif score > 0.8:
            return cls.HIGH
        elif score >= 0.5:
            return cls.MEDIUM
        else:
            return cls.LOW
    
    @property
    def threshold(self) -> float:
        """Get minimum threshold for this quality level"""
        thresholds = {
            QualityLevel.HIGH: 0.8,
            QualityLevel.MEDIUM: 0.5,
            QualityLevel.LOW: 0.0,
            QualityLevel.UNKNOWN: 0.0
        }
        return thresholds[self]
    
    @property
    def is_high_quality(self) -> bool:
        """Check if this is high quality"""
        return self == QualityLevel.HIGH
    
    @property
    def is_medium_quality(self) -> bool:
        """Check if this is medium quality"""
        return self == QualityLevel.MEDIUM
    
    @property
    def is_low_quality(self) -> bool:
        """Check if this is low quality"""
        return self == QualityLevel.LOW
    
    @property
    def is_unknown_quality(self) -> bool:
        """Check if quality is unknown"""
        return self == QualityLevel.UNKNOWN
    
    def __str__(self) -> str:
        """String representation"""
        return self.value
    
    def __repr__(self) -> str:
        """Debug representation"""
        return f"QualityLevel.{self.name}"
