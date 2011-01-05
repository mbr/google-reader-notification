#!/usr/bin/env python

import libgreader
import cairo
import gtk
import rsvg
import Image

from login import *

auth = libgreader.ClientAuth(username, password)
reader = libgreader.GoogleReader(auth)

#reader.buildSubscriptionList()

#unread = sum( feed.unread for feed in reader.feeds if feed.unread )

#print "unread:",unread

def convert_format(data, width, height, in_format, out_format):
	print "converting from %s to %s" % (in_format, out_format)

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
		print "on size changed"
		self.size = size	
		
		# create new pixbuf with correct size
		self.redraw()

	def redraw(self):
		# create new cairo surface
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.size, self.size)

		# context scaled to 1.0/1.0
		cr = cairo.Context(surface)
		cr.scale(self.size, self.size)

		# render background
		cr.save()
		cr.scale(1./self.svg_handle.get_property('width'), 1./self.svg_handle.get_property('height'))
		self.svg_handle.render_cairo(cr)
		cr.restore()

		# fetch
		pixbuf = pixbuf_from_surface(surface)

		# set icon from pixbuf
		self.set_from_pixbuf(pixbuf)

if '__main__' == __name__:
	icon = FeedIcon('Feed-icon.svg')
	
	gtk.main()
