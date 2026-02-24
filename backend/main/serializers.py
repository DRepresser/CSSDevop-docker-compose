from rest_framework import serializers
from django.db.models import Avg
from .models import Resume, Skill, Education, PreviousJob, Rating


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school_name', 'degree', 'start_date', 'end_date', 'description']


class PreviousJobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = PreviousJob
        fields = ['id', 'company_name', 'position', 'start_date', 'end_date', 'description']


class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    previous_jobs = PreviousJobSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    owner_full_name = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = [
            'id', 'owner', 'owner_username', 'owner_full_name',
            'profile_image', 'success_summary',
            'skills', 'education', 'previous_jobs',
            'avg_rating', 'created_at', 'updated_at',
        ]

    def get_avg_rating(self, obj):
        result = obj.ratings.aggregate(avg=Avg('score'))['avg']
        return round(result, 2) if result is not None else None

    def get_owner_full_name(self, obj):
        return f"{obj.owner.first_name} {obj.owner.last_name}".strip() or obj.owner.username
