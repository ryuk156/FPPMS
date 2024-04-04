from django.db.models import fields
from rest_framework import serializers
from FPPMS.models import Proposalmodel


class AdminSerializationClass(serializers.ModelSerializer):
    assignedTo = serializers.SerializerMethodField()

    class Meta:
        model = Proposalmodel
        fields = '__all__'

    def get_assignedTo(self, obj):
        return [user.username for user in obj.assignedTo.all()]
        
