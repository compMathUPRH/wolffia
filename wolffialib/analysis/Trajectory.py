
class Trajectory:
	def __init__(self, mixture, pcb):
		self.mixture = mixture
		self.pcbs = list()
		self.frames = list()
	
	def addFrame(self, coordinates, box):
		self.pcbs.append(box)
		self.frames.append(coordinates)
	
	def addFrames(self, frames, boxes):
		assert len(frames) == len(boxes)
		self.pcbs += boxes
		self.frames += frames
		
	def __iter__(self):
		self.position = -1
		return self
	
	def next(self):	
		self.position += 1
		if self.position > len(self.frames):
			raise StopIteration
		return  (frames[self.position], self.pcbs[self.position])
	
	def clear(self):
		self.frames = list()
		self.pcbs = list()
