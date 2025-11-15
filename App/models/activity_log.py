from datetime import datetime
from App.database import db


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 'hours', 'milestone', 'accolade'
    detail = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "category": self.category,
            "detail": self.detail,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
