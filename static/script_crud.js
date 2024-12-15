function editWorker(id, nama, kontak) {
    $('#editWorkerId').val(id);
    $('#editWorkerNama').val(nama);
    $('#editWorkerKontak').val(kontak);
    $('#editWorkerModal').modal('show');
  }
  
  function deleteWorker(id) {
    if (confirm('Apakah Anda yakin ingin menghapus pekerja ini?')) {
      window.location.href = `/delete_worker/${id}`;
    }
  }
  