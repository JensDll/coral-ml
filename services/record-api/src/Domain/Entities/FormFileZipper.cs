using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    public class FormFileZipper
    {
        private readonly FormFileZipEntry[] _formFileZipEntries;

        public FormFileZipper(params FormFileZipEntry[] formFileZipEntries)
        {
            _formFileZipEntries = formFileZipEntries;
        }

        public async Task<byte[]> CreateZipAsync()
        {
            using var memoryStream = new MemoryStream();

            using (var archive = new ZipArchive(memoryStream, ZipArchiveMode.Create, true))
            {
                foreach (var entry in _formFileZipEntries)
                {
                    var zipEntry = archive.CreateEntry(entry.EntryName, CompressionLevel.Optimal);
                    using var zipEntryStream = zipEntry.Open();
                    await entry.File.CopyToAsync(zipEntryStream);
                }
            }

            return memoryStream.ToArray();
        }
    }
}
