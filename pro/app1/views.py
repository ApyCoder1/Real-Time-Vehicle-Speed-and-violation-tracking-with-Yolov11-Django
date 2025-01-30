from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpeedRecord
from .serializers import SpeedRecordSerializer
from django.shortcuts import render
from django.db.models import Count, Avg, Max
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import Http404
from .models import SpeedRecord

class SpeedRecordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SpeedRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        records = SpeedRecord.objects.all()
        serializer = SpeedRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
####################################################################

# View to display the list of speed records
def speed_records(request):
    # Fetch all records from the SpeedRecord model
    records = SpeedRecord.objects.all()

    # Handle record deletion
    if request.method == "POST":
        # Get the ID of the record to delete from the request
        record_id = request.POST.get('delete_id')
        try:
            # Try to get and delete the record
            record = SpeedRecord.objects.get(id=record_id)
            record.delete()
        except SpeedRecord.DoesNotExist:
            raise Http404("Record not found.")

        # Redirect to the same page to refresh the list after deletion
        return redirect('speed_records')

    # Pass records to the template
    return render(request, 'speed_records.html', {'records': records})


def dashboard(request):
    # Fetch the total number of vehicles tracked
    total_vehicles = SpeedRecord.objects.count()

    # Calculate average speed
    avg_speed = SpeedRecord.objects.aggregate(Avg('speed'))['speed__avg']

    # Get the top 5 fastest vehicles
    top_5_fastest = SpeedRecord.objects.order_by('-speed')[:5]

    # Speed violation records (for example: speed > 80 km/h)
    speed_limit = 10
    speed_violations = SpeedRecord.objects.filter(speed__gt=speed_limit).count()

    # Vehicle count by track
    vehicle_count_by_track = SpeedRecord.objects.values('track_id').annotate(count=Count('track_id'))

    # Speed distribution (can be displayed as a histogram in the frontend)
    speed_distribution = SpeedRecord.objects.values('speed').annotate(count=Count('speed'))

    # Vehicles by time of day (let's categorize into Morning (6AM-12PM), Afternoon (12PM-6PM), Evening (6PM-12AM))
    morning = SpeedRecord.objects.filter(time__hour__gte=6, time__hour__lt=12).count()
    afternoon = SpeedRecord.objects.filter(time__hour__gte=12, time__hour__lt=18).count()
    evening = SpeedRecord.objects.filter(time__hour__gte=18, time__hour__lt=24).count()

    # Recent records
    recent_records = SpeedRecord.objects.all().order_by('-date', '-time')[:5]

    context = {
        'total_vehicles': total_vehicles,
        'avg_speed': avg_speed,
        'top_5_fastest': top_5_fastest,
        'speed_violations': speed_violations,
        'vehicle_count_by_track': vehicle_count_by_track,
        'speed_distribution': speed_distribution,
        'morning': morning,
        'afternoon': afternoon,
        'evening': evening,
        'recent_records': recent_records
    }

    return render(request, 'dashboard.html', context)

