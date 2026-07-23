from django.core.management.base import BaseCommand
from core.models import Stat, Track, Value, TeamMember


STATS = [
    (1,  '5,000+', 'Registered Builders'),
    (2,  '$150K+', 'Total Prize Pool'),
    (3,  '48 Hrs', 'Hack Window'),
    (4,  '6',      'Challenge Tracks'),
    (5,  '30+',    'Countries'),
    (6,  '120+',   'Expert Mentors'),
]

TRACKS = [
    (1,  '01', '🤖', 'AI & Machine Learning',
     'Build intelligent systems that adapt, learn, and make decisions. '
     'From edge inference to multimodal models — if it involves a neural network, it belongs here.',
     '$25,000', 'AI / ML'),
    (2,  '02', '🌐', 'Open Web Infrastructure',
     'Decentralize, secure, and accelerate the web. P2P protocols, privacy tooling, '
     'and the plumbing that millions will depend on.',
     '$20,000', 'Web3 / OSS'),
    (3,  '03', '🏥', 'Health & Biotech',
     'Diagnostics, assistive devices, clinical workflows, and tools that make healthcare more human. '
     'Technology that touches lives.',
     '$22,000', 'HealthTech'),
    (4,  '04', '⚡', 'Climate & Energy',
     'Grid intelligence, carbon tracking, renewable management. '
     'Model, predict, and optimize — hack the energy transition.',
     '$20,000', 'CleanTech'),
    (5,  '05', '🎓', 'Future of Learning',
     'Adaptive curricula, spatial learning, AI tutors. '
     'Reimagine how humans acquire skills — education that meets the learner where they are.',
     '$18,000', 'EdTech'),
    (6,  '06', '🔬', 'Deep Tech Wildcard',
     'Photonics, quantum, robotics, materials. If it is hard, weird, and might change everything '
     '— submit here. No brief. Full freedom.',
     '$30,000', 'Wildcard'),
]

VALUES = [
    (1, 'D', 'Depth over Performance',
     'We judge on technical validity and real-world applicability, not pitch polish. '
     'A working prototype with honest limitations will always beat a beautiful slide deck. '
     'Mentors come to look at code, not presentations.'),
    (2, 'C', 'Collision is the Method',
     'Disciplinary boundaries exist because institutions created them, not because nature respects them. '
     'We structure teams, tracks, and feedback loops to maximise unexpected intersections. '
     'The collision is the point.'),
    (3, 'S', 'Ship, Then Reflect',
     'Done beats perfect. Paralysis is the enemy of learning. We reward teams who build something real '
     'and can articulate clearly what they would do differently with more time — '
     'that combination tells you everything.'),
    (4, 'O', 'Open by Default',
     'All Parallax submissions are open-sourced under MIT on day one. '
     'The ecosystem benefits when ideas compound. Participants retain IP rights but release code freely '
     '— because the best version of your idea needs others to build on it.'),
]

TEAM = [
    (1, 'Rohan Mehta',  'Co-founder',        '🧬',
     'ML researcher at a genomics lab. Believes every biological problem is also a data problem, and vice versa.'),
    (2, 'Lena Fischer',  'Co-founder',        '🏗️',
     'Computational architect turned systems designer. Has a habit of asking "but what does the structure tell you?" in every meeting.'),
    (3, 'Zara Okonkwo',  'Head of Operations','⚡',
     'Power systems engineer who ran the first Parallax hub in Lagos. Keeps six timezones in her head at once.'),
    (4, 'Aditya Rao',    'Head of Tracks',    '🔬',
     'Materials scientist and science communicator. Designs the challenge briefs so they are hard enough to matter and open enough to surprise.'),
]


class Command(BaseCommand):
    help = 'Seeds initial Parallax content: stats, tracks, values, team members.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding stats ...')
        Stat.objects.all().delete()
        for order, number, label in STATS:
            Stat.objects.create(order=order, number=number, label=label)

        self.stdout.write('Seeding tracks ...')
        Track.objects.all().delete()
        for order, index, icon, name, desc, prize, tag in TRACKS:
            Track.objects.create(
                order=order, index=index, icon=icon, name=name,
                description=desc, prize=prize, tag=tag,
            )

        self.stdout.write('Seeding values ...')
        Value.objects.all().delete()
        for order, letter, title, desc in VALUES:
            Value.objects.create(order=order, letter=letter, title=title, description=desc)

        self.stdout.write('Seeding team ...')
        TeamMember.objects.all().delete()
        for order, name, role, emoji, bio in TEAM:
            TeamMember.objects.create(
                order=order, name=name, role=role, avatar_emoji=emoji, bio=bio,
            )

        self.stdout.write(self.style.SUCCESS('Done — database seeded.'))
