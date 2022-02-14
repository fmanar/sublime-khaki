import sublime
import sublime_plugin


def Filter_Select(matches, selection):
	# return matches contained in selection
	result = []
	m, s = 0, 0
	while m < len(matches) and s < len(selection):
		mat = matches[m]
		sel = selection[s]
		if sel.contains(mat):
			if sel.a <= sel.b:
				res = sublime.Region(mat.a, mat.b)
			else:
				res = sublime.Region(mat.b, mat.a)
			result.append(res)
			m += 1
		elif mat.begin() < sel.end():
			m += 1
		else:
			s += 1
	return result


def Filter_Remove(matches, selection):
	# return selection minus contained matches
	result = []
	m, s = 0, 0
	flag_split = False
	while m < len(matches) and s < len(selection):
		mat = matches[m]
		sel = selection[s]
		if sel.contains(mat):
			if sel.a <= sel.b:
				res = sublime.Region(sel.a, mat.a)
				sel.a = mat.b
			else:
				res = sublime.Region(mat.a, sel.b)
				sel.b = mat.b
			result.append(res)
			flag_split = True
			m += 1
		elif mat.begin() < sel.end():
			m += 1
		else:
			result.append(sel)
			s += 1
	if flag_split:
		result.append(sel)
	# add any remaining selections
	while s < len(selection):
		result.append(selection[s])
		s += 1
	return result


def Filter_Keep(matches, selection):
	# keep selection regions with matches
	result = []
	m, s = 0, 0
	while m < len(matches) and s < len(selection):
		mat = matches[m]
		sel = selection[s]
		if sel.contains(mat):
			result.append(sel)
			m += 1
			s += 1
		elif mat.begin() < sel.end():
			m += 1
		else:
			s += 1
	return result


def Filter_Drop(matches, selection):
	# keep selection regions without matches
	result = []
	m, s = 0, 0
	while m < len(matches) and s < len(selection):
		mat = matches[m]
		sel = selection[s]
		if sel.contains(mat):
			m += 1
			s += 1
		elif mat.begin() < sel.end():
			m += 1
		else:
			result.append(sel)
			s += 1
	while s < len(selection):
		result.append(selection[s])
		s += 1
	return result


#
# One-Shot Commands
#
class _KhFilterBase(sublime_plugin.TextCommand):
	'''Base class for one-shot filtering.

	Apply regex and filter to selection, no questions asked.

	Override _filter to change behavior.
	
	'''
	def run(self, edit, regex):
		matches = self.view.find_all(regex)
		selection = self.view.sel()
		result = self._filter(matches, selection)
		selection.clear()
		selection.add_all(result)

	def _filter(self, matches, selection):
		raise NotImplementedError


class KhSelect(_KhFilterBase):
	def _filter(self, matches, selection):
		return Filter_Select(matches, selection)


class KhRemove(_KhFilterBase):
	def _filter(self, matches, selection):
		return Filter_Remove(matches, selection)


class KhKeep(_KhFilterBase):
	def _filter(self, matches, selection):
		return Filter_Keep(matches, selection)


class KhDrop(_KhFilterBase):
	def _filter(self, matches, selection):
		return Filter_Drop(matches, selection)


#
# Interactive Commands
#
class _KhInteractiveFilterBase(sublime_plugin.TextCommand):
	'''Base class for interactive filtering.

	Pops up input widget to prompy for regex and displays results in 
	real time.

	Override _filter in child classes to change behavior.

	'''
	input_caption = "Base"
	empty_result_is_init = False
	region_scope = "region.cyanish"

	def run(self, edit):
		sel = self.view.sel()
		self.view.add_regions("bu_init", sel, scope=self.region_scope, flags=sublime.DRAW_NO_FILL)
		self.view.add_regions("bu_result", sel, scope=self.region_scope)
		sel.clear()
		view_input = self.view.window().show_input_panel(self.input_caption, "", self.on_done, self.on_change, self.on_cancel)
		view_input.assign_syntax("Packages/Regular Expressions/RegExp.sublime-syntax")

	def on_done(self, regex):
		sel = self.view.sel()
		sel.clear()
		regions = self.view.get_regions("bu_result")
		sel.add_all(regions)
		self.view.erase_regions("bu_init")
		self.view.erase_regions("bu_result")

	def on_change(self, regex):
		if len(regex) == 0:
			if self.empty_result_is_init:
				result = self.view.get_regions("bu_init")
			else:
				result = []
			self.view.add_regions("bu_result", result, scope=self.region_scope)
			return
		matches = self.view.find_all(regex)
		selection = self.view.get_regions("bu_init")
		result = self._filter(matches, selection)
		self.view.add_regions("bu_result", result, scope=self.region_scope)

	def on_cancel(self):
		self.view.sel().add_all(self.view.get_regions("bu_init"))
		self.view.erase_regions("bu_init")
		self.view.erase_regions("bu_result")

	def _filter(self, matches, selection):
		raise NotImplementedError


class KhInteractiveSelect(_KhInteractiveFilterBase):
	input_caption = "Select"
	empty_result_is_init = False
	def _filter(self, matches, selection):
		return Filter_Select(matches, selection)


class KhInteractiveRemove(_KhInteractiveFilterBase):
	input_caption = "Remove"
	empty_result_is_init = True
	def _filter(self, matches, selection):
		return Filter_Remove(matches, selection)
	

class KhInteractiveKeep(_KhInteractiveFilterBase):
	input_caption = "Keep"
	empty_result_is_init = False
	def _filter(self, matches, selection):
		return Filter_Keep(matches, selection)


class KhInteractiveDrop(_KhInteractiveFilterBase):
	input_caption = "Drop"
	empty_result_is_init = True
	def _filter(matches, selection):
		return Filter_Drop(matches, selection)

