from rest_framework import serializers
from .models import *
from users.models import Availability


def get_video_token(obj):
    return obj.generate_video_token()


class AppointmentSerializer(serializers.ModelSerializer):
    video_token = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['patient', 'status', 'created_at']

        def validate(self, data):
            doctor = data['doctor']
            date = data['date']
            start_time = data['start_time']
            end_time = data['end_time']

            # Ensure time validity
            if start_time >= end_time:
                raise serializers.ValidationError("Start time must be before end time.")

            # Check if doctor has availability on this day
            weekday = date.strftime('%A')
            doctor_availabilities = Availability.objects.filter(
                doctor=doctor,
                day_of_week=weekday
            )

            valid_slot = False
            for slot in doctor_availabilities:
                if slot.start_time <= start_time and slot.end_time >= end_time:
                    valid_slot = True
                    break
            if not valid_slot:
                raise serializers.ValidationError("This time is outside the doctor's available hours.")

            # Check for overlapping appointments for this doctor
            doctor_conflicts = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status__in=['pending', 'confirmed']
            )
            if doctor_conflicts.exists():
                raise serializers.ValidationError("This time slot is already booked for the doctor.")

            # Optional: Check if patient has another appointment at the same time
            patient = self.context['request'].user
            patient_conflicts = Appointment.objects.filter(
                patient=patient,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status__in=['pending', 'confirmed']
            )
            if patient_conflicts.exists():
                raise serializers.ValidationError("You already have an appointment at this time.")

            return data

