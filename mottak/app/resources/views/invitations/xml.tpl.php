{% extends:'body' %}

{% block:content %}
<form method="post" enctype="multipart/form-data">
	<div class="form-group">
		<label for="archiveFile">XML-fil</label>
		<div class="custom-file">
			<input type="file" name="archive" class="custom-file-input" id="archiveFile">
			<label class="custom-file-label" for="archiveFile">Velg fil</label>
		</div>
	</div>
	<button type="submit" class="btn btn-primary">Last opp</button>
</form>

<script>
$('#archiveFile').on('change',function() {
	var fileName = $(this).val();
	$(this).next('.custom-file-label').html(fileName.replace('C:\\fakepath\\', ''));
})
</script>
{% endblock %}
