<?php

namespace app\http\controllers;

use app\http\input\CreateInput;
use app\http\input\XmlInput;
use app\models\ArchiveType;
use app\models\Invitation;
use mako\http\exceptions\NotFoundException;
use mako\http\response\senders\Redirect;
use mako\http\routing\Controller;
use mako\validator\input\traits\InputValidationTrait;
use mako\view\ViewFactory;

/**
 *
 */
class Invitations extends Controller
{
	use InputValidationTrait;

	/**
	 *
	 */
	public function start(ViewFactory $view): string
	{
		return $view->render('invitations.xml');
	}

	/**
	 *
	 */
	public function parseXml(): Redirect
	{
		$input = $this->validate(XmlInput::class);

		$xml = simplexml_load_file($input['archive']->getRealPath());

		// Find the UUID and checksum

		$uuid = str_replace('UUID:', '', (string) $xml->attributes()['OBJID']);

		$checksum = (string) $xml->fileSec->fileGrp->file->attributes()['CHECKSUM'];

		$name = $email = null;

		// Try to find the submitter

		foreach($xml->metsHdr->agent as $agent)
		{
			$attributes = $agent->attributes();

			if((string) $attributes['OTHERROLE'] === 'SUBMITTER' && (string) $attributes['TYPE'] === 'INDIVIDUAL')
			{
				$name = (string) $agent->name;

				foreach($agent->note as $note)
				{
					if(strpos((string) $note, '@') !== false)
					{
						$email = (string) $note;
					}
				}

				break;
			}
		}

		// Flash the data and redirect to the next form

		$this->session->putFlash('archive', compact('uuid', 'checksum', 'name', 'email'));

		return $this->redirectResponse('invitations.create');
	}

	/**
	 *
	 */
	public function create(): string
	{
		$input = $this->session->getFlash('archive');

		return $this->view->render('invitations.create',
		[
			'input'         => $input,
			'archive_types' => ArchiveType::ascending('type')->all(),
		]);
	}

	/**
	 *
	 */
	public function store(): Redirect
	{
		$input = $this->validate(CreateInput::class);

		$invitation = new Invitation;

		$invitation->archive_type_id = $input['archive_type_id'];

		$invitation->uuid = $input['uuid'];

		$invitation->checksum = $input['checksum'];

		$invitation->is_sensitive = $input['is_sensitive'] === '1' ? true : false;

		$invitation->name = $input['name'];

		$invitation->email = $input['email'];

		$invitation->save();

		return $this->redirectResponse('invitations.receipt', ['id' => $invitation->id]);
	}

	/**
	 *
	 */
	public function receipt(string $id): string
	{
		$invitation = Invitation::get($id);

		if(!$invitation)
		{
			throw new NotFoundException;
		}

		$url = 'dpldr://' . base64_encode(json_encode
		([
			'reference'  => $invitation->uuid,
			'uploadUrl'  => getenv('UPLOAD_URL'),
			'uploadType' => 'tar',
			'meta'       => ['invitation_id' => $invitation->id],
		]));

		return $this->view->render('invitations.receipt',
		[
			'invitation' => $invitation,
			'url'        => $url,
		]);
	}
}
