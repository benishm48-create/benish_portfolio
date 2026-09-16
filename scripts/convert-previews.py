from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
for kind in ['hero','about']:
 path=root/'public'/'models'/f'{kind}-preview.png'
 Image.open(path).save(path.with_suffix('.webp'),quality=88)
