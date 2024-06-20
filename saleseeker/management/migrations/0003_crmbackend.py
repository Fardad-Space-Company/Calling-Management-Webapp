# Generated by Django 2.2 on 2024-06-20 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_postcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='CRMbackend',
            fields=[
                ('EmployeeID', models.CharField(max_length=11)),
                ('DealStatus', models.CharField(choices=[('hang_up', 'Hang Up'), ('not_interested', 'Not Interested'), ('gate_keeper', 'Gate Keeper'), ('decision_maker', 'Decision Maker'), ('call_appointment', 'Call Appointment'), ('visit_appointment', 'Visit Appointment'), ('follow_up', 'Follow Up'), ('visited', 'Visited'), ('voice_mail', 'Voice Mail'), ('no_answer', 'No Answer')], default='hang_up', max_length=20)),
                ('ShopName', models.CharField(max_length=100)),
                ('Date', models.TextField()),
                ('CallDuration', models.TextField(blank=True, null=True)),
                ('Email', models.CharField(blank=True, max_length=50, null=True)),
                ('Appointement_Date', models.TextField(blank=True, null=True)),
                ('OWname', models.CharField(blank=True, max_length=20, null=True)),
                ('OWnum', models.CharField(blank=True, max_length=15, null=True)),
                ('GKname', models.CharField(blank=True, max_length=20, null=True)),
                ('GKnum', models.CharField(blank=True, max_length=15, null=True)),
                ('Note', models.TextField(blank=True, null=True)),
                ('Shop_Status', models.CharField(choices=[('junk_lead', 'Junk Lead'), ('qualified', 'Qualified'), ('prospecting', 'Prospecting'), ('onboarded', 'Onboarded'), ('no_answer', 'No Answer')], default='junk_lead', max_length=20)),
                ('AutoId', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'CRMbackend',
            },
        ),
    ]
