from rest_framework import serializers
from .models import Project, Task, User


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        write_only=True, help_text="Enter Your Email", required=True)
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = u'Email cannot be blank!'
        self.fields['email'].error_messages['required'] = u'The email field is required'
        self.fields['password'].error_messages['required'] = u'The password field is required'
        self.fields['password'].error_messages['blank'] = u'Password cannot be blank!'


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at')

    def __init__(self, *args, **kwargs):
        super(ProjectCreateSerializer, self).__init__(*args, **kwargs)
        self.fields['name'].error_messages['blank'] = u'Project Name field cannot be blank'
        self.fields['name'].error_messages['required'] = u'Project Name field is required'
        self.fields['description'].error_messages['blank'] = u'Project Description field cannot be blank'
        self.fields['description'].error_messages['required'] = u'Project Description field is required'

    def create(self, validated_data):
        user = self.context.get("user")
        project_instance = Project.objects.create(owner = self.context.get("user"), **validated_data)
        return project_instance
    

class ProjectEditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required = False)
    description = serializers.CharField(required = False)

    def __init__(self, *args, **kwargs):
        super(ProjectEditSerializer, self).__init__(*args, **kwargs)
        self.fields['id'].error_messages['blank'] = u'Project id field cannot be blank'
        self.fields['id'].error_messages['required'] = u'Project id field is required'

    def validate(self, data):
        print(data.get('id'))
        if not Project.objects.filter(owner = self.context.get("user"), id = data.get('id')).exists():
            raise serializers.ValidationError('Project does not exists.')
        
        return data
    
    def create(self, validated_data):
        Project.objects.filter(owner = self.context.get("user"), 
                               id = validated_data.get('id')).update(
                                                            owner = self.context.get("user"), **validated_data
                                                            # name = validated_data.get('name'),
                                                            # description = validated_data.get('description')
                                                        )
        return True
    

class TaskCreateSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField()
    class Meta:
        model = Task
        fields = ('id', 'name', 'description','assign_to', 'completed', 'project_id')

    def __init__(self, *args, **kwargs):
        super(TaskCreateSerializer, self).__init__(*args, **kwargs)
        self.fields['project_id'].error_messages['blank'] = u'Project ID field cannot be blank'
        self.fields['project_id'].error_messages['required'] = u'Project ID field is required'
        self.fields['name'].error_messages['blank'] = u'Task Name field cannot be blank'
        self.fields['name'].error_messages['required'] = u'Task Name field is required'
        self.fields['description'].error_messages['blank'] = u'Task Description field cannot be blank'
        self.fields['description'].error_messages['required'] = u'Task Description field is required'

    def validate(self, data):
        print(data.get('project_id'))
        if not Project.objects.filter(id = data.get('project_id')).exists():
            raise serializers.ValidationError('Project does not exists.')
       
        if data.get('assign_to'):
            if not User.objects.filter(id = data.get('assign_to').id).exists():
                raise serializers.ValidationError('Given assign_to id does not exist')
        
        return data
    
    def create(self, validated_data):
        if validated_data.get('assign_to'):
            Task.objects.create(project=Project.objects.get(id = validated_data.get('project_id')),
                            assign_to = User.objects.get(id = validated_data.pop('assign_to').id),
                            **validated_data)
        else:    
            Task.objects.create(project=Project.objects.get(id = validated_data.get('project_id')),
                             **validated_data)
        return validated_data
    

class TaskEditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required = False)
    description = serializers.CharField(required = False)
    assign_to = serializers.IntegerField(required = False)
    completed = serializers.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(TaskEditSerializer, self).__init__(*args, **kwargs)
        self.fields['id'].error_messages['blank'] = u'Task id field cannot be blank'
        self.fields['id'].error_messages['required'] = u'Task id field is required'

    def validate(self, data):
        if not Task.objects.filter(id = data.get('id')).exists():
            raise serializers.ValidationError('Task does not exists.')
        
        if data.get('assign_to'):
            if not User.objects.filter(id = data.get('assign_to')).exists():
                raise serializers.ValidationError('Given assign_to id does not exist')
        
        return data
    
    def create(self, validated_data):
        if validated_data.get('assign_to'):
            Task.objects.filter(id = validated_data.get('id')).update(
                                                        assign_to = User.objects.get(id = validated_data.pop('assign_to')),
                                                        **validated_data
                                                    )
        else:
            Task.objects.filter(id = validated_data.get('id')).update(
                                                    **validated_data
                                                )
        return True

