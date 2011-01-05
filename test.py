#!/usr/bin/env python

import math

import libgreader
import cairo
import gtk
import gobject
import rsvg
import Image

from login import *

def convert_format(data, width, height, in_format, out_format):
	# PIL uses big-endian as well
	img = Image.frombuffer(
		out_format,
		(width, height),
		data,
		'raw',
		in_format,
		0,
		1
	)

	return img.tostring('raw', out_format, 0, 1)


def pixbuf_from_surface(surface):
	# GDKs format: RGBA or RGB, big endian byte order
	# cairos format: ARGB or XRGB, little endian byte order
	#             => BGRA or BGRX
	#                             (at least on x86/AMD64)
	if cairo.FORMAT_ARGB32 == surface.get_format():
		in_format = 'BGRA'
		out_format = 'RGBA'
		alpha = True
		stride = surface.get_width()*4
	elif cairo.FORMAT_RGB24 == surface.get_format():
		in_format = 'BGRX'
		out_format = 'RGB'
		alpha = False
		stride = surface.get_width()*3
	else: raise Exception('Can only handle RGB or RGBA formats.')

	data = convert_format(
		surface.get_data(),
		surface.get_width(),
		surface.get_height(),
		in_format,
		out_format
	)

	pixbuf = gtk.gdk.pixbuf_new_from_data(
		data = data,
		colorspace = gtk.gdk.COLORSPACE_RGB,
		has_alpha = alpha,
		bits_per_sample = 8,
		width = surface.get_width(),
		height = surface.get_height(),
		rowstride = stride
	)

	return pixbuf


class FeedIcon(gtk.StatusIcon):
	def  __init__(self, background_file, *args, **kwargs):
		super(FeedIcon, self).__init__(*args, **kwargs)
		self.unread_count = 0
		self.connect('size-changed', self.on_size_changed, None)

		# load background
		self.svg_handle = rsvg.Handle(file = background_file)

	def on_size_changed(self, status_icon, size, statusicon):
		self.size = size	
		
		# create new pixbuf with correct size
		self.redraw()

	def redraw(self):
		# create new cairo surface
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.size, self.size)

		# context scaled to 1.0/1.0
		cr = cairo.Context(surface)
		cr.scale(self.size, self.size)

		# leave a little room
		cr.scale(0.8, 0.8)
		cr.translate(0.1, 0.1)

		# render background
		cr.save()
		cr.scale(1./self.svg_handle.get_property('width'), 1./self.svg_handle.get_property('height'))
		self.svg_handle.render_cairo(cr)
		cr.restore()

		# draw on top if there are new items
		if self.unread_count:
			cr.set_source_rgba(0, 0, 0.8, 0.7)

			# c_x, c_y is the circle center
			c_x = 0.6
			c_y = 0.6
			radius = 0.38

			cr.arc(c_x, c_y, radius, 0, math.pi*2)
			cr.fill()

			# assume each number is about square
			text = str(self.unread_count)
			if len(text) > 2: text = '+'
			cr.set_font_size(radius*1.7/len(text))
			cr.select_font_face("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

			x_bearing, y_bearing, width, height, x_advance, y_advance = cr.text_extents(text)
			cr.move_to(c_x-width/2, c_y+height/2)

			cr.set_source_rgb(1, 1, 1)
			cr.show_text(text)

		# fetch
		pixbuf = pixbuf_from_surface(surface)

		# set icon from pixbuf
		self.set_from_pixbuf(pixbuf)


class GoogleReaderIcon(FeedIcon):
	icon_file = 'Feed-icon.svg'
	def __init__(self, username, password):
		super(GoogleReaderIcon, self).__init__(self.icon_file)
		auth = libgreader.ClientAuth(username, password)
		self.reader = libgreader.GoogleReader(auth)
		self.timeout_source = None

	@property
	def unread_count(self):
		self.update()
		return self._unread_count

	@unread_count.setter
	def unread_count(self, val):
		self._unread_count = val

	def update(self):
		self.reader.buildSubscriptionList()
		self._unread_count = sum( feed.unread for feed in self.reader.feeds if feed.unread )

	def set_update_interval(self, seconds):
		def call_update():
			self.redraw()
			return True

		if self.timeout_source: gobject.source_remove(self.timeout_source)

		self.timeout_source = gobject.timeout_add(seconds * 1000, call_update) # every 5 minutes


if '__main__' == __name__:
	icon = GoogleReaderIcon(username, password)
	icon.set_update_interval(5*60)
	
	gtk.main()
