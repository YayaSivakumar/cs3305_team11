import random

def generate_filename():
    # Define a list of sample file names and extensions
    file_names = [
        'report', 'invoice', 'letter', 'meeting_notes', 'presentation',
        'contract', 'manual', 'recipe', 'schedule', 'summary',
        'proposal', 'article', 'review', 'guide', 'plan',
        'chart', 'analysis', 'budget', 'agenda', 'minutes',
        'newsletter', 'brochure', 'diagram', 'drawing', 'blueprint',
        'outline', 'project', 'feedback', 'assessment', 'message',
        'chapter', 'lecture', 'notes', 'draft', 'document',
        'checklist', 'profile', 'biography', 'study', 'overview',
        'statement', 'release', 'notification', 'memo', 'update'
    ]

    file_extensions = [
        'txt', 'pdf', 'doc', 'docx', 'xls',
        'xlsx', 'ppt', 'pptx', 'md', 'csv',
        'json', 'xml', 'html', 'css', 'js',
        'py', 'java', 'c', 'cpp', 'rb',
        'sql', 'log', 'dat', 'tar',
        'zip', 'rar', 'jpg', 'jpeg', 'png',
        'gif', 'bmp', 'tiff', 'mp3', 'wav',
        'mp4', 'avi', 'mov', 'flv', 'mkv'
    ]

    # Generate a random list of 50 files with random extensions
    random_files = [f"{random.choice(file_names)}_{i}.{random.choice(file_extensions)}" for i in range(50)]

    return random_files
