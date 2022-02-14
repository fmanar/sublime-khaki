import sublime
import sublime_plugin

class KhExitInsertModeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.settings().set('command_mode', True)
		self.view.settings().set('inverse_caret_state', True)
		# ensure all selections are at least size 1
		selection = self.view.sel()
		result = []
		for s in selection:
			if s.size() == 0:			
				r = sublime.Region(s.a - 1, s.b)
			else:
				r = s
			result.append(r)
		selection.clear()
		selection.add_all(result)
		self.view.set_status('mode', "COMMAND MODE")


class KhEnterInsertModeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.settings().set('command_mode', False)
		self.view.settings().set('inverse_caret_state', False)
		# shrink all selections to 0
		selection = self.view.sel()
		result = []
		for s in selection:
			result.append(sublime.Region(s.b, s.b))
		selection.clear()
		selection.add_all(result)
		self.view.set_status('mode', "INSERT MODE")


class KhPrintRowCol(sublime_plugin.TextCommand):
	def run(self, edit):
		sel = self.view.sel()
		region = sel[0]
		print("region:", region)
		print("rowcol:", self.view.rowcol(region.a))
		print("rowcol_utf8:", self.view.rowcol_utf8(region.a))
		print("rowcol_utf16:", self.view.rowcol_utf16(region.a))
		print("point:",self.view.text_point(*self.view.rowcol(region.a)))

class KhPrintSelection(sublime_plugin.TextCommand):
	def run(self, edit):
		selection = self.view.sel()
		for region in selection:
			print("({}, {}) xpos={}".format(region.a, region.b, region.xpos))


def GetAnchorAndCaret(region):
	'''Return the locations of a regions anchor and caret.

	Locations are text points.  Conceptually they include the character after them.
	E.g. the anchor is always a full character corresponding to a Region(anchor, anchor + 1).

	These functions ease thinking about ranges as inclusive of the endpoint in both directions.

	'''
	if region.a < region.b:
		anchor = region.a
		caret = region.b - 1
	elif region.a > region.b:
		anchor = region.a - 1
		caret = region.b
	else:
		anchor = region.a
		caret = region.b
	return anchor, caret

def SetAnchorAndCaret(anchor, caret, xpos=-1):
	'''Return a the region corresponding to anchor and caret.'''
	if anchor <= caret:
		return sublime.Region(anchor, caret + 1, xpos)
	elif anchor > caret:
		return sublime.Region(anchor + 1, caret, xpos)


class KhMoveByCharacter(sublime_plugin.TextCommand):
	# use delta/count instead of forward?
	def run(self, edit, delta=1, extend=False):
		selection = self.view.sel()
		result = []
		for region in selection:
			a, c = GetAnchorAndCaret(region)
			c += delta
			if not extend:
				a = c
			result.append(SetAnchorAndCaret(a, c))
		selection.clear()
		selection.add_all(result)	
		

class KhMoveByLine(sublime_plugin.TextCommand):
	'''Move vertically.

	Uses vertical displacement in screen space, and saves horizontal
	position.

	'''
	def run(self, edit, delta=1, extend=False):
		selection = self.view.sel()
		result = []
		for region in selection:
			a, c = GetAnchorAndCaret(region)
			x, y = self.view.text_to_layout(c)
			if region.xpos == -1:
				xpos = x
			else:
				xpos = region.xpos
			y += delta * self.view.line_height()
			c = self.view.layout_to_text((xpos, y))
			if not extend:
				a = c
			result.append(SetAnchorAndCaret(a, c, xpos))
		selection.clear()
		selection.add_all(result)	


class KhSplitSelectionIntoLines(sublime_plugin.TextCommand):
	def run(self, edit):
		sel = self.view.sel()
		result = []
		for region in sel:
			result += self.view.split_by_newlines(region)
		sel.clear()
		sel.add_all(result)
