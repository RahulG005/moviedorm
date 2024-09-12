from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)
        #fields = "__all__"


# class WatchListSerializer(serializers.ModelSerializer):
#     # reviews = ReviewSerializer(many=True, read_only=True)
#     platform = serializers.CharField(source='platform.name')

#     class Meta:
#         model = WatchList
#         fields = "__all__"
    
class WatchListSerializer(serializers.ModelSerializer):
    # Accept 'platform' as a string and validate it
    platform = serializers.CharField(required = False) 

    class Meta:
        model = WatchList
        fields = "__all__"

    def validate_platform(self, value):
        """
        Validate that the platform exists in the database.
        """
        try:
            platform_instance = StreamPlatform.objects.get(name=value)
        except StreamPlatform.DoesNotExist:
            raise serializers.ValidationError("Platform with this name does not exist.")
        return platform_instance

    def create(self, validated_data):
        # Extract platform name and validate
        platform_instance = self.validate_platform(validated_data.pop('platform'))
        # Create the WatchList object
        watchlist = WatchList.objects.create(platform=platform_instance, **validated_data)
        return watchlist

    def update(self, instance, validated_data):
        # Optionally update the platform field if it is provided
        platform_name = validated_data.pop('platform', None)
        if platform_name:
            platform_instance = self.validate_platform(platform_name)
            instance.platform = platform_instance

        # Update the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated instance
        instance.save()
        return instance
    

    

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"


# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different!")
#         else:
#             return data

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value