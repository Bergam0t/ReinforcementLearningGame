extends Popup

func _on_DismissAutoTimer_timeout():
	get_tree().paused = false
	self.hide()