"""Explicit arithmetic terminal condition on wellformed restricted counter lists."""
def terminal(state):
 if state['phase']!='front' or state['right']['z']!=1:return False
 tokens=state['right']['tokens']
 if not tokens or tokens[0][0]!=1:return False
 if tokens[0][1]is None or tokens[0][1]==2:return True
 if tokens[0][1]!=1:return False
 i=1
 while i<len(tokens):
  b,g=tokens[i]
  if b!=2:return False
  if g is None or g==2:return True
  if g!=1:return False
  i+=1
 return False
